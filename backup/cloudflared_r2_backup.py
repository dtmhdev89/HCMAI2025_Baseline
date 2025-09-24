from minio import Minio
from minio.error import S3Error
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import islice


def download_object(client, bucket_name, object_name, local_file):
    """Helper function to download a single object."""
    try:
        os.makedirs(os.path.dirname(local_file), exist_ok=True)
        print(f"⬇️ Downloading: {object_name} → {local_file}")
        client.fget_object(bucket_name, object_name, local_file)
        return f"✅ {object_name}"
    except Exception as e:
        return f"❌ {object_name}: {e}"


def chunked_iterable(iterable, size):
    """Chia iterator thành batch nhỏ."""
    it = iter(iterable)
    while True:
        batch = list(islice(it, size))
        if not batch:
            break
        yield batch


def backup_r2_bucket(endpoint, access_key, secret_key, bucket_name, local_backup_dir,
                     max_workers=8, batch_size=1000):
    """
    Download all objects from a Cloudflare R2 bucket to a local folder using MinIO client
    with parallel downloads and batch processing.
    """
    client = Minio(
        endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=True  # Cloudflare R2 requires HTTPS
    )

    os.makedirs(local_backup_dir, exist_ok=True)

    try:
        objects = client.list_objects(bucket_name, recursive=True)

        for batch_num, batch in enumerate(chunked_iterable(objects, batch_size), start=1):
            print(f"\n📦 Processing batch {batch_num} ({len(batch)} objects) ...")

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_obj = {
                    executor.submit(
                        download_object,
                        client,
                        bucket_name,
                        obj.object_name,
                        os.path.join(local_backup_dir, obj.object_name)
                    ): obj.object_name
                    for obj in batch
                }

                for future in as_completed(future_to_obj):
                    result = future.result()
                    print(result)

        print("\n🎉 Backup completed successfully.")

    except S3Error as e:
        print("❌ Error occurred:", e)


if __name__ == "__main__":
    LOCAL_BACKUP_DIR = "./r2_backup"

    R2_ENDPOINT = os.getenv("R2_ENDPOINT")
    R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
    R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
    R2_BUCKET = os.getenv("R2_BUCKET")

    backup_r2_bucket(
        endpoint=R2_ENDPOINT,
        access_key=R2_ACCESS_KEY,
        secret_key=R2_SECRET_KEY,
        bucket_name=R2_BUCKET,
        local_backup_dir=LOCAL_BACKUP_DIR,
        max_workers=16,     # số luồng tải song song
        batch_size=1000      # số object xử lý trong 1 batch
    )
