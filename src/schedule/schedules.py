from src.services.price import check_price_interval
from datetime import datetime, timezone
from lib.logger import logger


class ScheduleService(object):
    
    @staticmethod   
    def check_price():
        
        # _datetime_second = str(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()).split(".")[0]   
        check_price_interval()
           
            
  