# dialogical_net Skill on Picroft
# Author: Tony Higuchi (hello@tonyhiguchi.com)
#
# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.messagebus.message import Message
from mycroft.util.log import getLogger
from OSC import OSCClient, OSCMessage, OSCServer

logger = getLogger(__name__)

# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.


class Misnomia(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(Misnomia, self).__init__(name="Misnomia")
        self.level = 1
        self.server = OSCServer("localhost", 5005)
        self.server.addMsgHandler("/disable", handle_disable)
        self.server.addMsgHandler("/enable", handle_enable)
        self.client = OSCClient()
        self.client.connect("localhost", 5005)
        self.processing = OSCClient()
        self.processing.connect("localhost", 5006)
        self.enabled = False

    def initialize(self):
        logger.info('Initializing dialogical_net...')
        self._register_event_handlers()

    def _register_event_handlers(self):
        self.add_event('recognizer_loop:wakeword', self.handle_awoken)
        self.add_event('recognizer_loop:utterance', self.handle_utterance)
        logger.info('registering event...')

    # The "handle_xxxx_intent" function is triggered by Mycroft when the
    # skill's intent is matched.  The intent is defined by the IntentBuilder()
    # pieces, and is triggered when the user's utterance matches the pattern
    # defined by the keywords.  In this case, the match occurs when one word
    # is found from each of the files:
    #    vocab/en-us/Hello.voc
    #    vocab/en-us/World.voc
    # In this example that means it would match on utterances like:
    #   'Hello world'
    #   'Howdy you great big world'
    #   'Greetings planet earth'
    @intent_handler(IntentBuilder("").require("lvl1"))
    def handle_lvl1_intent(self, message):
        # In this case, respond by simply speaking a canned response.
        # Mycroft will randomly speak one of the lines from the file
        #    dialogs/en-us/hello.world.dialog
        if self.level >= 1 and self.enabled:
            self.pathra_speak("lvl1bag")

    @intent_handler(IntentBuilder("").require("sol1"))
    def handle_sol1_intent(self, message):
        # In this case, respond by simply speaking a canned response.
        # Mycroft will randomly speak one of the lines from the file
        #    dialogs/en-us/hello.world.dialog
        if self.level == 1 and self.enabled:
            self.nextLevel(2)

    @intent_handler(IntentBuilder("").require("lvl2"))
    def handle_lvl2_intent(self, message):
        # In this case, respond by simply speaking a canned response.
        # Mycroft will randomly speak one of the lines from the file
        #    dialogs/en-us/hello.world.dialog
        if self.level >= 2 and self.enabled:
            self.pathra_speak("lvl2bag")

    @intent_handler(IntentBuilder("").require("sol2"))
    def handle_sol2_intent(self, message):
        # In this case, respond by simply speaking a canned response.
        # Mycroft will randomly speak one of the lines from the file
        #    dialogs/en-us/hello.world.dialog
        if self.level == 2 and self.enabled:
            self.nextLevel(3)

    @intent_handler(IntentBuilder("").require("lvl3"))
    def handle_lvl3_intent(self, message):
        # In this case, respond by simply speaking a canned response.
        # Mycroft will randomly speak one of the lines from the file
        #    dialogs/en-us/hello.world.dialog
        if self.level >= 3 and self.enabled:
            self.pathra_speak("lvl3bag")

    # @intent_handler(IntentBuilder("").require("sol3"))
    # def handle_file_reset_configuration_intent(self, message):
    #     # In this case, respond by simply speaking a canned response.
    #     # Mycroft will randomly speak one of the lines from the file
    #     #    dialogs/en-us/hello.world.dialog
    #     if self.level == 3:
    #         self.reset()

    @intent_handler(IntentBuilder("").require("reset"))
    def handle_reset_intent(self, message):
        # In this case, respond by simply speaking a canned response.
        # Mycroft will randomly speak one of the lines from the file
        #    dialogs/en-us/hello.world.dialog
        self.reset()

    def nextLevel(self, lvl):
        self.level = lvl
        logger.info('Next Level! ' + self.level)
        self.processing.send(OSCMessage("/level", self.level))
        self.speak_dialog(message)

    def reset(self):
        self.level = 1
        logger.info('Reset!' + self.level)
        self.client.send(OSCMessage("/level", self.level))
        self.speak_dialog(message)

    def pathra_speak(self, message):
        logger.info('Pathra speaks!')
        self.client.send(OSCMessage("/pathraspeak", message))
        self.processing.send(OSCMessage("/pathraspeak", message))
        self.speak_dialog(message)

    def handle_awoken(self, event):
        logger.info('Misnomia Awoke!')
        self.client.send(OSCMessage("/awoken", event))

    def handle_utterance(self, event):
        logger.info('player spoke!')
        self.processing.send(OSCMessage("/playerspeak", event))

    def handle_disable(self, event):
        logger.info('pathra disabled!')
        self.enabled = False

    def handle_enable(self, event):
        logger.info('pathra enabled!')
        self.enabled = True

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #    return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.


def create_skill():
    return Misnomia()
