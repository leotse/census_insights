from typing import List

from sqlalchemy import func, select, or_

from api_models import LngLat
from decorators import use_db
from models.age_group import AgeGroup
from models.dissemination_area import DisseminationArea


@use_db
def query_stats_by_lnglats(lnglats: List[LngLat], *, session=None):
    if not lnglats:
        return []

    # sum age groups
    query = session.query(
        func.sum(AgeGroup.total).label("total"),
        func.sum(AgeGroup.age_0_to_4).label("age_0_to_4"),
        func.sum(AgeGroup.age_5_to_9).label("age_5_to_9"),
        func.sum(AgeGroup.age_10_to_14).label("age_10_to_14"),
        func.sum(AgeGroup.age_15_to_19).label("age_15_to_19"),
        func.sum(AgeGroup.age_20_to_24).label("age_20_to_24"),
        func.sum(AgeGroup.age_25_to_29).label("age_25_to_29"),
        func.sum(AgeGroup.age_30_to_34).label("age_30_to_34"),
        func.sum(AgeGroup.age_35_to_39).label("age_35_to_39"),
        func.sum(AgeGroup.age_40_to_44).label("age_40_to_44"),
        func.sum(AgeGroup.age_45_to_49).label("age_45_to_49"),
        func.sum(AgeGroup.age_50_to_54).label("age_50_to_54"),
        func.sum(AgeGroup.age_55_to_59).label("age_55_to_59"),
        func.sum(AgeGroup.age_60_to_64).label("age_60_to_64"),
        func.sum(AgeGroup.age_65_to_69).label("age_65_to_69"),
        func.sum(AgeGroup.age_70_to_74).label("age_70_to_74"),
        func.sum(AgeGroup.age_75_to_79).label("age_75_to_79"),
        func.sum(AgeGroup.age_80_to_84).label("age_80_to_84"),
        func.sum(AgeGroup.age_85_plus).label("age_85_plus"),
    )

    # join AgeGroup and DisseminationArea tables..
    query = query.filter(DisseminationArea.dissemination_area_id == AgeGroup.geo_code)

    # by input locations
    location_filters = [
        func.ST_Contains(DisseminationArea.geometry, f"SRID=4326;POINT({lnglat.lng} {lnglat.lat})")
        for lnglat in lnglats
    ]
    query = query.filter(or_(*location_filters))

    aggregated = query.first()
    return {
        "total": aggregated.total,
        "age_0_to_4": aggregated.age_0_to_4,
        "age_5_to_9": aggregated.age_5_to_9,
        "age_10_to_14": aggregated.age_10_to_14,
        "age_15_to_19": aggregated.age_15_to_19,
        "age_20_to_24": aggregated.age_20_to_24,
        "age_25_to_29": aggregated.age_25_to_29,
        "age_30_to_34": aggregated.age_30_to_34,
        "age_35_to_39": aggregated.age_35_to_39,
        "age_40_to_44": aggregated.age_40_to_44,
        "age_45_to_49": aggregated.age_45_to_49,
        "age_50_to_54": aggregated.age_50_to_54,
        "age_55_to_59": aggregated.age_55_to_59,
        "age_60_to_64": aggregated.age_60_to_64,
        "age_65_to_69": aggregated.age_65_to_69,
        "age_70_to_74": aggregated.age_70_to_74,
        "age_75_to_79": aggregated.age_75_to_79,
        "age_80_to_84": aggregated.age_80_to_84,
        "age_85_plus": aggregated.age_85_plus,
    }


@use_db
def query_stats_by_ids(dissemination_area_ids: List[str], *, session=None):
    if not dissemination_area_ids:
        return []

    age_groups = (
        session.query(
            func.sum(AgeGroup.total).label("total"),
            func.sum(AgeGroup.age_0_to_4).label("age_0_to_4"),
            func.sum(AgeGroup.age_5_to_9).label("age_5_to_9"),
            func.sum(AgeGroup.age_10_to_14).label("age_10_to_14"),
            func.sum(AgeGroup.age_15_to_19).label("age_15_to_19"),
            func.sum(AgeGroup.age_20_to_24).label("age_20_to_24"),
            func.sum(AgeGroup.age_25_to_29).label("age_25_to_29"),
            func.sum(AgeGroup.age_30_to_34).label("age_30_to_34"),
            func.sum(AgeGroup.age_35_to_39).label("age_35_to_39"),
            func.sum(AgeGroup.age_40_to_44).label("age_40_to_44"),
            func.sum(AgeGroup.age_45_to_49).label("age_45_to_49"),
            func.sum(AgeGroup.age_50_to_54).label("age_50_to_54"),
            func.sum(AgeGroup.age_55_to_59).label("age_55_to_59"),
            func.sum(AgeGroup.age_60_to_64).label("age_60_to_64"),
            func.sum(AgeGroup.age_65_to_69).label("age_65_to_69"),
            func.sum(AgeGroup.age_70_to_74).label("age_70_to_74"),
            func.sum(AgeGroup.age_75_to_79).label("age_75_to_79"),
            func.sum(AgeGroup.age_80_to_84).label("age_80_to_84"),
            func.sum(AgeGroup.age_85_plus).label("age_85_plus"),
        )
        .filter(AgeGroup.geo_code.in_(dissemination_area_ids))
        .first()
    )
    return {
        "total": age_groups.total,
        "age_0_to_4": age_groups.age_0_to_4,
        "age_5_to_9": age_groups.age_5_to_9,
        "age_10_to_14": age_groups.age_10_to_14,
        "age_15_to_19": age_groups.age_15_to_19,
        "age_20_to_24": age_groups.age_20_to_24,
        "age_25_to_29": age_groups.age_25_to_29,
        "age_30_to_34": age_groups.age_30_to_34,
        "age_35_to_39": age_groups.age_35_to_39,
        "age_40_to_44": age_groups.age_40_to_44,
        "age_45_to_49": age_groups.age_45_to_49,
        "age_50_to_54": age_groups.age_50_to_54,
        "age_55_to_59": age_groups.age_55_to_59,
        "age_60_to_64": age_groups.age_60_to_64,
        "age_65_to_69": age_groups.age_65_to_69,
        "age_70_to_74": age_groups.age_70_to_74,
        "age_75_to_79": age_groups.age_75_to_79,
        "age_80_to_84": age_groups.age_80_to_84,
        "age_85_plus": age_groups.age_85_plus,
    }
