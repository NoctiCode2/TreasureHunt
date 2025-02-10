from MyAgent import MyAgent

from MyAgent import MyAgent

class MyAgentChest(MyAgent):
    def __init__(self, id, x, y, env, capacity=0):  # ✅ Ajout de capacity
        super().__init__(id, x, y, env, capacity)   # ✅ Passe capacity au parent



    def agir(self):
        """L'agent chest ouvre les coffres et envoie un message aux agents or ou pierres"""
        super().execute_task()

        if self.env.grilleTres[self.posX][self.posY]:  # Si un coffre est là
            coffre = self.env.grilleTres[self.posX][self.posY]
            if not coffre.isOpen():
                coffre.openChest()
                print(f"🔓 {self.id} a ouvert un coffre à ({self.posX}, {self.posY})")

                # 📩 Envoyer un message à l'agent approprié
                if coffre.getType() == 1:  # Trésor or
                    self.env.task_manager.send_message("gold", ("collect", self.posX, self.posY, coffre.getValue()))
                elif coffre.getType() == 2:  # Trésor pierres
                    self.env.task_manager.send_message("stones", ("collect", self.posX, self.posY, coffre.getValue()))
