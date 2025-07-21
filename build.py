import asyncio
from pathlib import Path

from src import (
    logger,
    Paratranz,
    ProjectDOL,
    PARATRANZ_TOKEN,
    CHINESE_VERSION,
    SOURCE_TYPE
)
from src.tools.process_variables import VariablesProcess as VP

async def process_common(dol_common: ProjectDOL, pt: Paratranz, chs_version: str):
    """
    Original version processing flow
    1. Download source code
    2. Create a raw dictionary
    3. Download a Chinese dictionary
    4. Replace the raw meat dictionary
    5. Replace the original game text
    """
    """ Delete the database and run away """
    await dol_common.drop_all_dirs()

    """ Download source code """
    await dol_common.download_from_gitgud()

    """ Preprocess all <<set>> """
    var = VP()
    var.fetch_all_file_paths()
    var.fetch_all_set_content()

    """ Creating a Raw Dictionary """
    await dol_common.create_dicts()

    """ Download the Chinese dictionary. The finished product is in the `raw_dicts` folder """
    download_flag = await pt.download_from_paratranz()  # If you download, you need to fill in the administrator's token in consts, find it in the website's personal settings
    if not download_flag:
        return

    """ Replace the raw dictionary """
    await dol_common.update_dicts()


async def main():
    logger.info(f"filepath: {Path(__file__)}")
    dol_common = ProjectDOL(type_=SOURCE_TYPE)  # Change to "dev" to download the latest development branch content common original version

    pt_common = Paratranz(type_=SOURCE_TYPE)
    if not PARATRANZ_TOKEN:
        logger.error("PARATRANZ_TOKEN is not filled in, the download of the Chinese package may fail. Please go to https://paratranz.cn/users/my to check your token in the settings column and fill it in .env\n")
        return

    await process_common(dol_common, pt_common, chs_version=CHINESE_VERSION)


if __name__ == '__main__':
     asyncio.run(main())
