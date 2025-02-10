
from MyAgentGold import MyAgentGold
from MyAgentStones import MyAgentStones
from MyAgentChest import MyAgentChest

class TaskManager:
    
    def __init__(self, env):
        self.env = env  #  Stocke l'environnement
        self.treasures_collected = {}
        self.score_global = 0
        self.messages = {"gold": [], "stones": []}
        self.task_queue = []  # Liste des tâches à faire

    def send_message(self, agent_type, task):
        """Ajoute un message à la file des agents or ou pierres"""
        self.messages[agent_type].append(task)

    def has_message(self, agent_id):
        """Vérifie si un message est disponible pour cet agent"""
        if "gold" in agent_id:
            return bool(self.messages["gold"])
        elif "stones" in agent_id:
            return bool(self.messages["stones"])
        return False

    def get_message(self, agent_id):
        """Récupère le premier message pour un agent"""
        if "gold" in agent_id and self.messages["gold"]:
            return self.messages["gold"].pop(0)
        elif "stones" in agent_id and self.messages["stones"]:
            return self.messages["stones"].pop(0)
        return None

    def update_score(self, agent_id, valeur):
        """ Mise à jour du score global"""
        if agent_id in self.treasures_collected:
            self.treasures_collected[agent_id] += valeur
        else:
            self.treasures_collected[agent_id] = valeur
        self.score_global += valeur
        print(f"🎯 Score mis à jour ({agent_id} a déposé {valeur} unités) : {self.score_global}")

    def detect_new_tasks(self):
        """Détecte les nouvelles tâches et les ajoute à la file"""
        self.task_queue = []  #  Nettoyage avant de détecter de nouvelles tâches
        for x in range(self.env.tailleX):
            for y in range(self.env.tailleY):
                if self.env.grilleTres[x][y]:
                    if not self.env.grilleTres[x][y].isOpen():
                        self.task_queue.append(("open", x, y))  # Coffre à ouvrir
                    else:
                        self.task_queue.append(("collect", x, y, self.env.grilleTres[x][y].getType()))  # Collecte du trésor

    def assign_tasks(self, agents):
        """Assigne des tâches aux agents en fonction de leur type"""
        for agent in agents.values():
            if not agent.task_list:  #  L'agent ne doit pas déjà être occupé
                for task in self.task_queue:
                    action, x, y = task[:3]
                    
                    # Si c'est une tâche "open" et que l'agent est un ouvreur de coffre
                    if action == "open" and isinstance(agent, MyAgentChest):
                        agent.task_list.append(task)
                        self.task_queue.remove(task)
                        print(f"📩 {agent.id} va ouvrir un coffre à {x, y}")
                        break  

                    #  Si c'est une tâche "collect" et que l'agent a la compétence requise
                    elif action == "collect":
                        tresor_type = task[3]  # Type de trésor à collecter

                        if ((tresor_type == 1 and isinstance(agent, MyAgentGold)) or 
                            (tresor_type == 2 and isinstance(agent, MyAgentStones))):
                            
                            #  Vérifier qu'aucun agent n'a déjà cette tâche
                            if not any(t[1] == x and t[2] == y for a in agents.values() for t in a.task_list):
                                agent.task_list.append(task)
                                self.task_queue.remove(task)
                                print(f"📩 {agent.id} va collecter un trésor à {x, y}")

                                #  Ajoute automatiquement la tâche de dépôt après collecte
                                agent.task_list.append(("deposit", self.env.posUnload[0], self.env.posUnload[1]))
                                break
                    