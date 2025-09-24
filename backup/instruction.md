## Instructions

### Install required libs:

Skip if installed

```
pip install -q minio
```

### Export environment
Replace your_key environment
Then run them on terminal to export environments

Or you can do any similar way

```bash
export R2_ACCESS_KEY=<your_key>
export R2_ENDPOINT=<your_key>
export R2_SECRET_KEY=<your_key>
export R2_BUCKET="demo-s3"
```


### Run the python file

Depend on your python, run one of them:

```bash
python backup/cloudflared_r2_backup.py
```

```bash
python3 backup/cloudflared_r2_backup.py
```
