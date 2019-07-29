from datetime import datetime
import psycopg2
from elastic.elasticsearch import Elastic


class BusScrapyPipeline(object):

    @staticmethod
    def convert_data_time(value):
        """
        prepared date value for saving
        :param value:
        :return:
        """
        return str(datetime.strptime(value, '%d.%m.%y %H:%M'))

    @staticmethod
    def try_float(value):
        """
        prepared float value for saving
        :param value:
        :return:
        """
        value =  value.replace('\xa0', '')
        try:
            value = float(value)
        except ValueError:
            value = None
        return value

    @staticmethod
    def try_int(value):
        """
        prepared int value for saving
        :param value:
        :return:
        """
        value = value.replace('\xa0', '')
        try:
            value = int(value)
        except ValueError:
            value = None
        return value

    def open_spider(self, spider):
        hostname = 'db'
        username = 'postgres'
        password = 'postgres'
        database = 'postgres'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

        self.es = Elastic()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        item.setdefault('place', None)
        commit_status = True
        try:
            self.cur.execute(
                """
                INSERT INTO inception_busstation (id, title, departure, voyage, arrival, cost, status, place) 
                VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (title, departure, voyage) DO UPDATE
                    SET arrival = excluded.arrival,
                        cost = excluded.cost,
                        status = excluded.status,
                        place = excluded.place;
                """, (item['title'], self.convert_data_time(item['departure']),
                      item['voyage'].replace('\xa0\xa0', '-').replace('#', ''), item['arrival'],
                      self.try_float(item['cost']), item['status'],
                      self.try_int(item['place']))
            )
            self.connection.commit()
        except:
            commit_status = False

        if commit_status:
            elastic_id = '{} {} {}'.format(item["title"],
                                           self.convert_data_time(item["departure"]),
                                           item["voyage"].replace("\xa0\xa0", "-").replace("#", ""))
            self.es.index_document(dict(item), elastic_id)

        return item
