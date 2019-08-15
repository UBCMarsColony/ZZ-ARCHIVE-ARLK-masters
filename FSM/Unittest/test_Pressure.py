from unittest import TestCase
from FSM.FSMDefinitions import PressureFSM
from FSM.Unittest.subsys_pressure import PressureSubsystem
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
outputs = [out1, out2, out3, out4, out5, out6, out7]  #LEDS


class FSMPressureUnittest(TestCase):
    """
    Unittest for the Pressure FSM.
    Inputs will be tested to trigger the correct state transitions.

    NOTE IF THE TESTS FAIL DUE TO SUBSYS ALREADY EXISTING IN POOL, REMOVE THE SS AFTER EACH UNITTEST.
    """

    # Test that State Machine starts in OFF state
    def test_initial_state(self):
        fsm = PressureFSM()
        self.assertEqual(fsm.current_state.name, 'idle')

    # Test input start pressurization
    def test_start_pressure(self):
        fsm = PressureFSM()
        ss = PressureSubsystem(name="Airlock Pressure", thread_id=t.airlock_press_ss_thread_id)
        ss.start()
        fsm.start_pressurize(ss, outputs)
        self.assertEqual(fsm.current_state.name, 'pressurize')
        remove(ss)  # KEEP ME IN OR TESTS FAIL

    def test_keep_pressurizing(self):
        fsm = PressureFSM()
        ss = PressureSubsystem(name="Airlock Pressure", thread_id=t.airlock_press_ss_thread_id)
        ss.start()
        fsm.start_pressurize(ss, outputs)
        fsm.keep_pressurize(ss, outputs)
        self.assertEqual(fsm.current_state.name, 'pressurize')
        remove(ss)

    def test_done_pressurize(self):
        fsm = PressureFSM()
        ss = PressureSubsystem(name="Airlock Pressure", thread_id=t.airlock_press_ss_thread_id)
        ss.start()
        fsm.start_pressurize(ss, outputs)
        fsm.done_pressurize(ss, outputs)
        self.assertEqual(fsm.current_state.name, 'idle')
        remove(ss)

    def test_start_depressure(self):
        fsm = PressureFSM()
        ss = PressureSubsystem(name="Airlock Pressure", thread_id=t.airlock_press_ss_thread_id)
        ss.start()
        fsm.start_depressurize(ss, outputs)
        self.assertEqual(fsm.current_state.name, 'depressurize')
        remove(ss)

    def test_keep_depressurize(self):
        fsm = PressureFSM()
        ss = PressureSubsystem(name="Airlock Pressure", thread_id=t.airlock_press_ss_thread_id)
        ss.start()
        fsm.start_depressurize(ss, outputs)
        fsm.keep_depressurize(ss, outputs)
        self.assertEqual(fsm.current_state.name, "depressurize")
        remove(ss)

    def test_done_depressurizing(self):
        fsm = PressureFSM()
        ss = PressureSubsystem(name="Airlock Pressure", thread_id=t.airlock_press_ss_thread_id)
        ss.start()
        fsm.start_pressurize(ss, outputs)
        fsm.done_pressurize(ss, outputs)
        fsm.start_depressurize(ss, outputs)
        fsm.done_depressurize(ss, outputs)
        self.assertEqual(fsm.current_state.name, "idle")
        remove(ss)

    def test_pause_pressurizing(self):
        fsm = PressureFSM()
        ss = PressureSubsystem(name="Airlock Pressure", thread_id=t.airlock_press_ss_thread_id)
        ss.start()
        fsm.start_pressurize(ss, outputs)
        fsm.pause_press(ss, outputs)
        self.assertEqual(fsm.current_state.name, 'pause')
        remove(ss)

    def test_pause_depressurizing(self):
        fsm = PressureFSM()
        ss = PressureSubsystem(name="Airlock Pressure", thread_id=t.airlock_press_ss_thread_id)
        ss.start()
        fsm.start_depressurize(ss, outputs)
        fsm.pause_depress(ss, outputs)
        self.assertEqual(fsm.current_state.name, 'pause')
        remove(ss)

    # For the meanings behind the emergency scenarios, refer to the documentation or FSM definition
    def test_detected_emerg_1(self):
        fsm = PressureFSM()
        ss = PressureSubsystem(name="Airlock Pressure", thread_id=t.airlock_press_ss_thread_id)
        ss.start()
        fsm.start_pressurize(ss, outputs)
        fsm.detected_emerg_1(ss, outputs)
        self.assertEqual(fsm.current_state.name, "Emergency")
        remove(ss)

    def test_detected_emerg_2(self):
        fsm = PressureFSM()
        ss = PressureSubsystem(name="Airlock Pressure", thread_id=t.airlock_press_ss_thread_id)
        ss.start()
        fsm.start_depressurize(ss, outputs)
        fsm.detected_emerg_2(ss, outputs)
        self.assertEqual(fsm.current_state.name, "Emergency")
        remove(ss)

    def test_detected_emerg_3(self):
        fsm = PressureFSM()
        ss = PressureSubsystem(name="Airlock Pressure", thread_id=t.airlock_press_ss_thread_id)
        ss.start()
        fsm.keep_idling(ss)
        fsm.detected_emerg_3(ss, outputs)
        self.assertEqual(fsm.current_state.name, "Emergency")
        remove(ss)

    def test_unresolved_emerg(self):
        fsm = PressureFSM()
        ss = PressureSubsystem(name="Airlock Pressure", thread_id=t.airlock_press_ss_thread_id)
        ss.start()
        fsm.keep_idling(ss)
        fsm.detected_emerg_3(ss, outputs)
        fsm.emerg_unresolved(ss, outputs)
        self.assertEqual(fsm.current_state.name, "Emergency")
        remove(ss)




