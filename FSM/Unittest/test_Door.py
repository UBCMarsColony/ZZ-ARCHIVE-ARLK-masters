from unittest import TestCase
from FSM.FSMDefinitions import DoorFSM
from FSM.Unittest.subsys_door import DoorSubsystem
from FSM.FSMMockClasses import MockOutput
from FSM.FSMConstants import Pins, ThreadIDs
from FSM.Unittest.subsys_pool import remove

p = Pins()
t = ThreadIDs()

out1 = MockOutput(name="Pressurize LED", pin=p.out1_pin)
out2 = MockOutput(name="In Progress LED", pin=p.out2_pin)
out3 = MockOutput(name="Depressurized LED", pin=p.out3_pin)
out4 = MockOutput(name='Enable', pin=p.out4_pin)
out5 = MockOutput(name="Confirm LED", pin=p.out5_pin)
out6 = MockOutput(name="Emergency LED", pin=p.out6_pin)
out7 = MockOutput(name="Pause LED", pin=p.out7_pin)
outputs = [out1, out2, out3, out4, out5, out6, out7]  # LEDS


class FSMDoorUnittest(TestCase):
    """
    Unittest for the Door FSM.
    Inputs will be tested to trigger the correct state transitions.

    NOTE IF THE TESTS FAIL DUE TO SUBSYS ALREADY EXISTING IN POOL, REMOVE THE SS AFTER EACH UNITTEST.
    """

    # Test that State Machine starts in OFF state
    def test_initial_state(self):
        fsm = DoorFSM()
        self.assertEqual(fsm.current_state.name, 'Idle')

    def test_start_open(self):
        fsm = DoorFSM()
        ss = DoorSubsystem(name="Test Door Subsystem", thread_id=t.airlock_door_ss_thread_id)
        ss.start()
        fsm.start_open(ss)
        self.assertEqual(fsm.current_state.name, 'Open')
        remove(ss)

    def test_keep_opening(self):
        fsm = DoorFSM()
        ss = DoorSubsystem(name="Test Door Subsystem", thread_id=t.airlock_door_ss_thread_id)
        ss.start()
        fsm.start_open(ss)
        fsm.keep_opening(ss)
        self.assertEqual(fsm.current_state.name, 'Open')
        remove(ss)

    def test_start_close(self):
        fsm = DoorFSM()
        ss = DoorSubsystem(name="Test Door Subsystem", thread_id=t.airlock_door_ss_thread_id)
        ss.start()
        fsm.start_close(ss)
        self.assertEqual(fsm.current_state.name, "Close")
        remove(ss)

    def test_keep_closing(self):
        fsm = DoorFSM()
        ss = DoorSubsystem(name="Test Door Subsystem", thread_id=t.airlock_door_ss_thread_id)
        ss.start()
        fsm.start_close(ss)
        fsm.keep_closing(ss)
        self.assertEqual(fsm.current_state.name, "Close")
        remove(ss)

    def test_done_open(self):
        fsm = DoorFSM()
        ss = DoorSubsystem(name="Test Door Subsystem", thread_id=t.airlock_door_ss_thread_id)
        ss.start()
        fsm.start_open(ss)
        fsm.done_open(ss)
        self.assertEqual(fsm.current_state.name, "Idle")
        remove(ss)

    def test_done_close(self):
        fsm = DoorFSM()
        ss = DoorSubsystem(name="Test Door Subsystem", thread_id=t.airlock_door_ss_thread_id)
        ss.start()
        fsm.start_close(ss)
        fsm.done_close(ss)
        self.assertEqual(fsm.current_state.name, "Idle")
        remove(ss)

    # For the meanings behind the emergency scenarios, refer to the documentation or FSM definition
    def test_detected_emerg_1(self):
        fsm = DoorFSM()
        ss = DoorSubsystem(name="Test Door Subsystem", thread_id=t.airlock_door_ss_thread_id)
        ss.start()
        fsm.start_open(ss)
        fsm.detected_emerg_1(ss)
        self.assertEqual(fsm.current_state.name, "Emergency")
        remove(ss)

    def test_detected_emerg_2(self):
        fsm = DoorFSM()
        ss = DoorSubsystem(name="Test Door Subsystem", thread_id=t.airlock_door_ss_thread_id)
        ss.start()
        fsm.start_close(ss)
        fsm.detected_emerg_2(ss)
        self.assertEqual(fsm.current_state.name, "Emergency")
        remove(ss)

    def test_detected_emerg_3(self):
        fsm = DoorFSM()
        ss = DoorSubsystem(name="Test Door Subsystem", thread_id=t.airlock_door_ss_thread_id)
        ss.start()
        fsm.detected_emerg_3(ss)
        self.assertEqual(fsm.current_state.name, "Emergency")
        remove(ss)

    def test_unresolved_emerg(self):
        fsm = DoorFSM()
        ss = DoorSubsystem(name="Test Door Subsystem", thread_id=t.airlock_door_ss_thread_id)
        ss.start()
        fsm.detected_emerg_3(ss)
        fsm.emerg_unresolved(ss)
        self.assertEqual(fsm.current_state.name, "Emergency")
        remove(ss)
