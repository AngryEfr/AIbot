from amplitude import Amplitude, BaseEvent
from config_data.config import Config, load_config


config: Config = load_config('.env')
amplitude = Amplitude(config.tg_bot.amplitude_token)


def track_user_register(user_id):
    event = BaseEvent(event_type="Sign Up", user_id=str(user_id))
    amplitude.track(event)


def change_character(change, user_id):
    event = BaseEvent(event_type="Character", user_id=str(user_id), event_properties={"change": change})
    amplitude.track(event)


def send_message(user_id, message):
    event = BaseEvent(event_type="Send Message", user_id=str(user_id), event_properties={"message": message})
    amplitude.track(event)


def take_answer(user_id, message):
    event = BaseEvent(event_type="Take Answer", user_id=str(user_id), event_properties={"message": message})
    amplitude.track(event)
