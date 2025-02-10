from MyAgent import MyAgent

class MyAgentGold(MyAgent):
    def __init__(self, id, x, y, capacity, env):
        super().__init__(id, x, y, env,capacity)
        self.capacity = capacity

    def agir(self):
        """L'agent vérifie les messages avant d'exécuter une tâche"""
        # 📨 Vérifie s'il y a des messages pour lui
        if self.env.task_manager.has_message(self.id):
            task = self.env.task_manager.get_message(self.id)
            if task[0] == "collect":
                self.task_list.append(task)  # Ajoute à sa liste de tâches

        super().execute_task()  # Continue avec l'exécution normale

        # Après collecte, aller au dépôt
        if self.treasure > 0:
            self.task_list.append(("deposit", self.env.posUnload[0], self.env.posUnload[1]))
