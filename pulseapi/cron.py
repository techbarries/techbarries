import logging
from datetime import datetime,timedelta
from fcm import Fcm
from authentication.serializers import DeviceSerializer
from authentication.models import Device, User
from general.models import Notification
from events.serializers import EventSerializer
from django.db.models import Q

from events.models import Event, EventStatus

# Get an instance of a logger
logger = logging.getLogger(__name__)

def my_scheduled_job():
    today=datetime.date(datetime.now())
    todayTime = datetime.now()
    dayAfter=today+timedelta(days=1);
    events=Event.objects.filter(event_start_date__range=[today,dayAfter]).all()
    serializer = EventSerializer(events, many=True)
    for event in serializer.data:
        if event["event_start_date"] and event["event_start_time"] is not None:
            date_time_str=event["event_start_date"]+" "+event["event_start_time"]
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            timediff=date_time_obj-todayTime
            tsecs = timediff.total_seconds()
            thrs = int(tsecs/(60*60))
            selectedEvent=Event.objects.filter(id=event["id"]).first()
            if selectedEvent is None:
                continue
            date=date_time_obj.strftime('%I:%M %p %A, %B %d, %Y')
            if thrs == 0 and not event["event_start_reminder_sent"]:
                selectedEvent.event_start_reminder_sent=True
                selectedEvent.save()
                desc="Your event "+event["name"]+" is starting @"+date
                details={"has_button":False,"id":event['id']}
                Notification.objects.create(title="Event Start",description=desc,redirect_to="EVENT_PAGE",details=details,user_id=User.objects.get(id=event["user_id"]))
                sentToUserDevices=Device.objects.filter(user_id=event["user_id"]).all()
                if sentToUserDevices.count()>0:
                    device_serializer=DeviceSerializer(sentToUserDevices,many=True)
                    for device in device_serializer.data:
                        if device['fcm_token'] is not None and len(device['fcm_token'])>0:
                            fcm=Fcm()
                            fcm.send(device['fcm_token'],"Event Start",desc,{"redirect_to":"EVENT_PAGE"})                

            if thrs == 12 and not event["reminder_sent"]:
                
                selectedEvent.reminder_sent=True
                selectedEvent.save()
                eventsToSend=EventStatus.objects.filter((Q(invited=True)|Q(paid=True)),event_id=event["id"]).values_list("user_id",flat=True)
                desc="Event "+event["name"]+" is starting @"+date
                for guest in eventsToSend:
                    details={"has_button":False,"id":event['id']}
                    Notification.objects.create(title="Upcoming Event",description=desc,redirect_to="EVENT_PAGE",details=details,user_id=User.objects.get(id=guest)) 
                    sentToUserDevices=Device.objects.filter(user_id=guest).all()
                    if sentToUserDevices.count()>0:
                        device_serializer=DeviceSerializer(sentToUserDevices,many=True)
                        for device in device_serializer.data:
                            if device['fcm_token'] is not None and len(device['fcm_token'])>0:
                                fcm=Fcm()
                                fcm.send(device['fcm_token'],"Upcoming Event",desc,{"redirect_to":"EVENT_PAGE"})
    logger.warning('===========================')
    logger.warning('CRON  was accessed at '+str(datetime.now())+' hours!')
    pass