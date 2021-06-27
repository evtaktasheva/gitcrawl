import psycopg2
import time
from github import Github
from tqdm import tqdm
from conf import DB_LOGIN, DB_PASSWORD, GITHUB_LOGIN, GITHUB_TOKEN

# authenticate to github
g = Github(GITHUB_LOGIN, GITHUB_TOKEN)

#  crawl GitHub for the links to files
#  get .py files from every 120 repos (theme: NLP) and sleep for an hour

for_db = []
repo_counter = 0
for i, repo in tqdm(enumerate(g.search_repositories("nlp" + "language:python"))):
    repo_counter += 1
    repo_link = 'https://api.github.com/repos/' + repo.full_name
    repo_name = repo.full_name
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            content = file_content.path
            if content.endswith('.py'):
                file_link = repo_link + '/contents/' + content
                file_path = content
                for_db.append((repo_name, file_link))

    if repo_counter == 120:
        print('\nGithub sleepy time\n')

        # connect to database
        conn = psycopg2.connect(dbname="qnkabsei",
                                user=DB_LOGIN,
                                password=DB_PASSWORD,
                                host="hattie.db.elephantsql.com")
        c = conn.cursor()

        for repo_name, file_link in tqdm(for_db, total=len(for_db)):
            try:
                c.execute("""INSERT INTO test (repo_name, file_link, seen)
                            VALUES (%s, %s, %s)""",
                          (repo_name, file_link, False))
            except:
                conn.rollback()

        #  save to database
        conn.commit()
        conn.close()

        #  clear the list for database and repos counter
        for_db = []
        repo_counter = 0

        #  sleep to not exceed the API rate limit
        time.sleep(3600)
