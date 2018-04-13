import requests
from bs4 import BeautifulSoup


class DailyNation:
    BASE_URL = 'https://www.nation.co.ke'

    @staticmethod
    def get_data(topic):
        """
        Get topic information based on the topic provided.
        :param topic:
        :return:
        """
        _topic = topic.lower()
        if _topic not in DailyNation.get_topics():
            raise ValueError('Topic does not exist')

        if _topic == 'photos':
            return DailyNation.get_photos(_topic)

        if _topic == 'videos':
            return DailyNation.get_videos(_topic)

        return DailyNation.get_topic_info(_topic)

    @staticmethod
    def get_html(url):
        """
        Get the Daily Nation html
        :return:
        """
        daily_nation = requests.get(url)
        html = BeautifulSoup(daily_nation.text, 'html.parser')
        return html

    @staticmethod
    def get_topics_lis():
        """
        Get all the lis in the nav bar
        :return:
        """
        html = DailyNation.get_html(DailyNation.BASE_URL)
        if html:
            nav = html.find('nav', class_='container')
            topics_ul = nav.find_all('ul')[1]
            return topics_ul.find_all('li')
        return None

    @staticmethod
    def get_topics():
        """
        Get all topics in the nav bar
        :return: list
        """
        lis = DailyNation.get_topics_lis()
        topics = []
        for li in lis:
            topics.append(li.find('a').text.lower())
        return topics

    @staticmethod
    def get_topics_url():
        """
        Get all topics in the nav bar with their corresponding urls
        :return:
        """
        lis = DailyNation.get_topics_lis()
        topics_with_url = {}
        for li in lis:
            topics_with_url[li.find('a').text.lower()] = li.find('a').get('href')
        return topics_with_url

    @staticmethod
    def get_topic_info(topic):
        """
        Get content for a given topic
        :param topic:
        :return:
        """
        topic_url = DailyNation.BASE_URL + DailyNation.get_topics_url()[topic.lower()]
        html = DailyNation.get_html(topic_url)
        if html:
            stories = []
            div_content = html.find('div', class_='five-eight column')
            stories_div = div_content.find_all('div', class_='story-teaser')
            for div in stories_div:
                story = {
                    'title': div.find('a').text, 'summary': div.find('p').text,
                    'story_url': div.find('a').get('href'),
                    'published_at': div.find('h6').text
                }
                if div.find('img'):
                    story['image_url'] = DailyNation.BASE_URL + div.find('img').get('src')
                story['image_url'] = ''
                stories.append(story)
            return stories

    @staticmethod
    def get_photos(topic):
        """
        Get all the images in the photos section
        :param topic:
        :return:
        """
        if topic != 'photos':
            raise ValueError('Topic should be photos')
        topic_url = DailyNation.BASE_URL + DailyNation.get_topics_url()[topic.lower()]
        html = DailyNation.get_html(topic_url)
        if html:
            images = {}
            images_list_div = html.find('div', class_='cb-content videolist')
            images_topics = images_list_div.find_all('div', class_='vh-caption')
            images_caption_headings = []
            for caption_div in images_topics:
                images_caption_headings.append(DailyNation.clean_string(caption_div.find('h3').text))
            image_rows_divs = images_list_div.find_all('div', class_='row')
            images_caption_headings_count = 0
            for images_item_div in image_rows_divs:
                trs = images_item_div.find('table').find_all('tr')
                items = []
                for tr in trs:
                    tds = tr.find_all('td')
                    for td in tds:
                        items.append({
                            'caption': td.find('div', class_='v-desc').find('a').text,
                            'image_url': DailyNation.BASE_URL + td.find('div', class_='v-img').find('img').get('src'),
                            'story_url': DailyNation.BASE_URL + td.find('div', class_='v-img').find('a').get('href')
                        })
                images[images_caption_headings[images_caption_headings_count]] = items
                images_caption_headings_count += 1
            return images

    @staticmethod
    def get_videos(topic):
        """
        Get all the videos in the photos section
        :param topic:
        :return:
        """
        if topic != 'videos':
            raise ValueError('Topic should be videos')
        topic_url = DailyNation.BASE_URL + DailyNation.get_topics_url()[topic.lower()]
        html = DailyNation.get_html(topic_url)
        if html:
            videos = {}
            videos_list_div = html.find('div', class_='cb-content videolist')
            videos_topics = videos_list_div.find_all('div', class_='vh-caption')
            videos_caption_headings = []
            for caption_div in videos_topics:
                videos_caption_headings.append(DailyNation.clean_string(caption_div.find('h3').text))
            video_rows_divs = videos_list_div.find_all('div', class_='row')
            videos_caption_headings_count = 0
            for videos_item_div in video_rows_divs:
                trs = videos_item_div.find('table').find_all('tr')
                items = []
                for tr in trs:
                    tds = tr.find_all('td')
                    for td in tds:
                        items.append({
                            'caption': td.find('div', class_='v-desc').text,
                            'image_url': td.find('div', class_='v-img').find('img').get('src'),
                            'story_url': DailyNation.BASE_URL + td.find(
                                'div',
                                class_='col-lg-3 col-xs-12 col-sm-6 videoitem'
                            ).find('a').get('href')
                        })
                videos[videos_caption_headings[videos_caption_headings_count]] = items
                videos_caption_headings_count += 1
            return videos

    @staticmethod
    def clean_string(string):
        new_string = string.replace('&nbsp', '')
        return new_string.replace(';', '')


