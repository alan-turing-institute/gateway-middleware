from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from azure.storage.blob import BlockBlobService

from simulate.config import CONFIG

JOB_ID = CONFIG["JOB_ID"]


def upload(fpath, sas_token):

    bs = BlockBlobService(account_name="simulate", sas_token=sas_token)

    origin = Path(fpath).resolve()
    destination = Path(JOB_ID).joinpath(fpath).as_posix()

    print("INFO: Uploading to cloud storage")
    print(f"\t{origin}")
    print(f"\t{destination}\n")

    bs.create_blob_from_path(
        container_name="openfoam-test-output", blob_name=destination, file_path=origin
    )


def zip_dir(zip_name, source_dir):
    src_path = Path(source_dir).expanduser().resolve(strict=True)
    with ZipFile(zip_name, "w", ZIP_DEFLATED) as zf:
        for file_ in src_path.rglob("*"):
            # exlude .zip to avoid recursion
            if file_.suffix not in [".zip", ".pyc"] and file_.stem not in [
                "__pycache__"
            ]:
                zf.write(file_, file_.relative_to(src_path.parent))
