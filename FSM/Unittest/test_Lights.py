from unittest import TestCase
from FSM.FSMDefinitions import LightFSM
from FSM.FSMMockClasses import MockLightSubsystem


class FSMLightsUnittest(TestCase):
    """
    Unittest for the Lights FSM.
    Inputs will be tested for the correct state transitions
    """
    # Test that State Machine starts in OFF state
    def test_initial_state(self):
        fsm = LightFSM()
        self.assertEqual(fsm.current_state.name, 'OFF')

    # Test input toggling turning on
    def test_turn_on(self):
        fsm = LightFSM()
        subsys = MockLightSubsystem("Lights Unittest")
        fsm.turn_on(subsys)
        self.assertEqual(fsm.current_state.name, "ON")

    # Test input toggling turning off
    def test_turn_off(self):
        fsm = LightFSM()
        subsys = MockLightSubsystem("Lights Unittest")
        fsm.turn_on(subsys)
        fsm.turn_off(subsys)
        self.assertEqual(fsm.current_state.name, "OFF")
