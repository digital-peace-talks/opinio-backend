from state.sessionstate import SessionState


class Sessions:
    def __init__(self):
        self.sessions = {}

    def register_session(self):
        state = SessionState()
        self.sessions[state.session_id] = state
        return state.session_id

    def get_session(self, session_id):
        if session_id not in self.sessions:
            return None
        return self.sessions[session_id]
