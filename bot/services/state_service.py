class StateService:
    @staticmethod
    def get_state(context, user_id: int) -> str:
        return context.application.bot_data.get("user_states", {}).get(user_id, "idle")

    @staticmethod
    def set_state(context, user_id: int, state: str):
        user_states = context.application.bot_data.setdefault("user_states", {})
        user_states[user_id] = state

    @staticmethod
    def reset_all(context):
        context.application.bot_data["user_states"] = {}

    @staticmethod
    def set_all(context, user_ids: list[int], state: str):
        user_states = context.application.bot_data.setdefault("user_states", {})
        for uid in user_ids:
            user_states[uid] = state