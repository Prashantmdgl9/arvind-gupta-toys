import streamlit as st
from bs4 import BeautifulSoup, SoupStrainer
import requests
import base64
from PIL import Image

def main():

    page = st.sidebar.selectbox("App Selections", ["URL Checker"])
    if page == "URL Checker":
        contact()
        #st.header("Checking for broken URLs on the site")
        broken_links()


def contact():
    set_png_as_page_bg('book2.jpg')
    st.title("A fistful of soil")
    st.header("“And somewhere there are engineers"
    " Helping others fly faster than sound."
    " But, where are the engineers"
    " helping those who must live on the ground?“")
    st.header("      "+ "                   - A Young Oxfam Poster")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: 2200px;
    background-repeat: no-repeat;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return



def broken_links():

    st.header("Checking URLs on https://www.arvindguptatoys.com/")
    url = 'https://www.arvindguptatoys.com/'
    broken_links_2(url)

def broken_links_2(url):

    page = requests.get(url)

    # Get the response code of given URL
    response_code = str(page.status_code)

    # Display the text of the URL in str
    data = page.text

    # Use BeautifulSoup to use the built-in methods
    soup = BeautifulSoup(data)

    # Iterate over all links on the given URL with the response code next to it

    tags = soup.find_all('a')

    urls = []

    for tag in tags:
        if tag.has_attr('href'):
            if(tag['href'].startswith('arvindgupta/')|tag['href'].startswith('chemistry-around.pdf')|tag['href'].startswith('nuffield-fertilizer')|tag['href'].startswith('soap-bubbles-mar.pdf')|
            tag['href'].startswith('guj-toy-treasures.pdf')|tag['href'].startswith('toys.html')|tag['href'].startswith('films.html')):
                urls.append('http://www.arvindguptatoys.com/'+tag['href'])
            else:
                if(len(tag['href'])>5):
                    urls.append(tag['href'])


    urls.pop(0)


    urls_y = []
    for url in urls:
        if "THE LITTLE LOG HOUSE" in url:
            print("1")
        elif url == "<li><a href=":
            print("2")
        elif url == "javascript:viewdiv(4)":
            print("3")
        elif url == "javascript:viewdiv(2)":
            print("4")
        elif url == "javascript:viewdiv(3)":
            print("5")
        elif "ahttps:" in url:
            url = url.replace("ahttps:", "https:")
            #print(url)
            urls_y.append(url)
        elif "hhttps:" in url:
            url = url.replace("hhttps:", "https:")
            #print(url)
            urls_y.append(url)
        elif "hthttps:" in url:
            url = url.replace("hthttps:", "https:")
            #print(url)
            urls_y.append(url)
        elif "\r\nhttps:" in url:
            url = url.replace("\r\nhttps:", "https:")
            #print(url)
            urls_y.append(url)
        else:
            urls_y.append(url)


    #st.write("The number of urls in this website are ", len(urls_y))
    st.metric(label="The number of urls in this website are", value=len(urls_y))
    st.subheader(" URL checking process is a little slow because of a many https://www.archive.org links, so it's better to select a range of URLs that you want to check")
    select_range(len(urls_y), urls_y)


def select_range(x, urls_y):
    st.write("Select a range: ")
    values = st.slider("Move the slider from both ends", 0, x, (200, 800))
    #st.write('Values:', values[0])
    st.write("Check the box to start the process")
    agree = st.checkbox('Run')
    if agree:
         st.write("Great! Let's go")
         links = find_broken_links(values[0], values[1], urls_y)
        # st.write("Broken links in the range are:")
        # for link in links:
        #     st.write(link)


def sanitize_url(beg, end, urls_y):
    url_t = urls_y[beg:end]
    url_a = []
    for x in url_t:
        if "\r\n" in x:
            x = x.replace("\r\n", "")
            url_a.append(x)
        else:
            url_a.append(x)
    return url_a

def find_broken_links(beg, end, urls_y):
    st.write("Broken links in the range are:")
    sanitized_urls = sanitize_url(beg, end, urls_y)
    st_links = []
    x = 1
    for t in sanitized_urls:
        print("Parsing :", x)
        x = x + 1
        code = parse(t)
        if code != 200:
            st_links.append(t)
            st.write(t)
    return st_links

def parse(url):
    try:
        code = requests.get(url).status_code
        #if requests.get(t).status_code != 200:
        #    st.append(t)
    except Exception as ex:
        print("Error occurred at " + url)
        code = 1
    return code


def about():
    return 0

if __name__ == "__main__":
    main()
