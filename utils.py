import requests
import base64
import psycopg2
from conf import DB_PASSWORD, DB_LOGIN, GITHUB_LOGIN, GITHUB_TOKEN


class Downloader(object):
    def __init__(self, file: str):
        self.id, self.file = file.split(maxsplit=1)

    def download(self):
        """
        Download the file
        :return: file content
        """
        # download file cintents
        filedata = requests.get(self.file, auth=(GITHUB_LOGIN, GITHUB_TOKEN))
        filedata = filedata.json()
        filename = filedata['name']
        filedata = base64.b64decode(filedata['content'])
        filedata = filedata.decode('utf-8')

        # connect to db
        conn = psycopg2.connect(
            dbname="qnkabsei",
            user=DB_LOGIN,
            password=DB_PASSWORD,
            host="hattie.db.elephantsql.com")
        cur = conn.cursor()

        # update file to seen
        query = "UPDATE gitcrawl SET seen = %s WHERE file_id = %s"
        cur.execute(query, (True, self.id,))

        # save to db
        cur.execute("INSERT INTO files VALUES (%s, %s, %s)",
                    (filename, self.file, filedata))
        conn.commit()
        conn.close()
