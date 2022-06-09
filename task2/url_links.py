import pandas as pd

url_list = [
    'https://www.google.com/search?q=caps&ei=zjCgYqmYMv7w4-EP19ewuAk&ved=0ahUKEwipt_-FjZ34AhV--DgGHdcrDJcQ4dUDCA0'
    '&uact=5&oq=caps&gs_lcp'
    '=Cgdnd3Mtd2l6EAMyBAgAEBMyBAgAEBMyBAgAEBMyBAgAEBMyBAgAEBMyBAgAEBMyBAgAEBMyBAgAEBMyBAgAEBMyBAgAEBM6BwgAEEcQsAM6CggAEEcQsAMQyQM6BwgAELADEENKBAhBGABKBAhGGABQ2gVYsw5gqxVoAnABeACAAaUBiAGKBZIBAzAuNJgBAKABAcgBCsABAQ&sclient=gws-wiz',
    'https://www.google.com/search?channel=fs&client=ubuntu&q=shoes',
    'https://www.google.com/search?channel=fs&client=ubuntu&q=mobiles']

urls = {"URL": url_list}
urls = pd.DataFrame(urls)
urls.to_csv("url_list.csv", index=False)
