import argparse
import ee
from datetime import datetime, timezone
from task_base import SCLTask


class SCLLandscapes(SCLTask):
    ee_rootdir = "projects/SCL/v1"
    # ee_pocdir = "{}/{}/geographies/Sumatra/scl_poly/{}"
    inputs = {
        "scl_eff_pot_hab": {
            "ee_type": SCLTask.FEATURECOLLECTION,
            "ee_path": "scl_path_species",
            "maxage": 1 / 365,  # years
        },
        "countries": {
            "ee_type": SCLTask.FEATURECOLLECTION,
            "ee_path": "USDOS/LSIB/2013",
            "maxage": 10,
        }
    }

    @property
    def ee_pocdir(self):
        return f"{self.species}/geographies/Sumatra/scl_poly/{self.taskdate}"

    def _scl_path(self, scltype):
        if scltype is None or scltype not in self.inputs:
            raise TypeError("Missing or incorrect scltype for setting scl path")
        return "{}/{}/geographies/Sumatra/scl_poly/{}/{}".format(
            self.ee_rootdir, self.species, self.taskdate, scltype
        )

    def scl_path_species(self):
        return self._scl_path("scl_eff_pot_hab")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_margin = ee.ErrorMargin(1)
        self.area_proj = "EPSG:5070"
        # self.countries = ee.FeatureCollection(self.inputs["countries"]["ee_path"])

    def calc(self):
        polys = ee.FeatureCollection(self.inputs['scl_eff_pot_hab']['ee_path'])

        core_species_Filter = ee.Filter.And(
            ee.Filter.lessThanOrEquals('min_patch_area', None, 'patch_area', None),
            # ee.Filter.lessThanOrEquals({'rightField': 'patch_area', 'leftField': 'min_patch_area'}),
            ee.Filter.eq('prob', 2),
            ee.Filter.eq('hii', 2)
        )

        core_survey_Filter = ee.Filter.And(
            ee.Filter.lessThanOrEquals('min_patch_area', None, 'patch_area', None),
            # ee.Filter.lessThanOrEquals({'rightField': 'patch_area', 'leftField': 'min_patch_area'}),
            ee.Filter.eq('prob', 1),
            ee.Filter.eq('hii', 2)
        )

        core_restoration_Filter = ee.Filter.And(
            ee.Filter.lessThanOrEquals('min_patch_area', None, 'patch_area', None),
            # ee.Filter.lessThanOrEquals({'rightField': 'patch_area', 'leftField': 'min_patch_area'}),
            ee.Filter.eq('prob', 1),
            ee.Filter.eq('hii', 3)
        )

        stepping_stone_Filter = ee.Filter.And(
            ee.Filter.greaterThan('min_patch_area', None, 'patch_area', None),
            ee.Filter.lessThanOrEquals('min_stp_stn_area', None, 'patch_area', None),
            ee.Filter.eq('prob', 2),
            ee.Filter.eq('hii', 2))

        fragment_Filter = ee.Filter.And(
            ee.Filter.greaterThan('min_patch_area', None, 'patch_area', None),
            ee.Filter.eq('prob', 2),
            ee.Filter.eq('hii', 2)
        )

        core_species = polys.filter(core_species_Filter)
        core_survey = polys.filter(core_survey_Filter)
        core_restoration = polys.filter(core_restoration_Filter)
        stepping_stones = polys.filter(stepping_stone_Filter)
        fragments = polys.filter(fragment_Filter)

        def feature_buffer(ft):
            return ft.buffer(2000)

        stepping_stones_con = stepping_stones.map(feature_buffer)

        fragments_con = fragments.map(feature_buffer)

        def scl_connectivity(ft):
            buffer = ft.buffer(2000)
            steppingStones = stepping_stones_con.filterBounds(buffer.geometry())
            frags = fragments_con.filterBounds(buffer.geometry())
            scl_merge = ee.FeatureCollection(buffer).merge(steppingStones).merge(frags)
            return scl_merge

        scl_species = core_species.map(scl_connectivity).flatten().union()

        scl_species_path = f"{self.ee_pocdir}/scl_species"

        scl_survey_path = f"{self.ee_pocdir}/scl_survey"

        scl_restoration_path = f"{self.ee_pocdir}/scl_restoration"

        # scl_fragment_path = "{self.ee_pocdir}/scl_fragment"
        # print(scl_species_path)
        self.export_fc_ee(scl_species, scl_species_path)
        self.export_fc_ee(core_survey, scl_survey_path)
        self.export_fc_ee(core_restoration, scl_restoration_path)
        # self.export_fc_ee(, scl_fragment_path)

    def check_inputs(self):
        super().check_inputs()


# -d 2016-01-01
# or --taskdate 2016-01-01
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--taskdate", default=datetime.now(timezone.utc).date())
    parser.add_argument("-s", "--species", default="Panthera_tigris")
    options = parser.parse_args()
    sclstats_task = SCLLandscapes(**vars(options))
    sclstats_task.run()
