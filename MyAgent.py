import random
class MyAgent:
    def __init__(self, id, x, y, env, capacity):
        self.id = id
        self.posX = x
        self.posY = y
        self.env = env
        self.task_list = []
        self.treasure = 0
        self.capacity = capacity
        self.is_chest = False
        self.mailBox = [] 

    def execute_task(self):
        from MyAgentGold import MyAgentGold  # ✅ Import différé
        from MyAgentStones import MyAgentStones
        from MyAgentChest import MyAgentChest
        """Exécute la tâche en cours si disponible"""
        if not self.task_list:
            return

        task = self.task_list[0]
        action, x, y = task[:3]

        # ✅ Vérifier si la case est occupée par un autre agent avant de bouger
        if self.is_position_occupied(x, y) and (x, y) != self.env.posUnload:
            print(f"❌ {self.id} ne peut pas aller à ({x}, {y}), case occupée.")
            return

        if action == "open" and isinstance(self, MyAgentChest):
            self.move_towards(x, y)
            
            if (self.posX, self.posY) == (x, y):  # ✅ L'agent est arrivé au coffre
                print(f"🔓 {self.id} a ouvert un coffre à ({x}, {y}) !")
                self.env.grilleTres[x][y].openChest()
                self.task_list.pop(0)  # ✅ Supprime la tâche "open"

                # ✅ Déterminer le type de trésor (1 = or, 2 = pierres)
                tresor_type = self.env.grilleTres[x][y].getType()
                # ✅ Trouver l'agent collecteur le plus proche
                closest_agent = None
                min_distance = float('inf')
                available_agents = []  # Liste des agents du bon type

                for agent in self.env.agentSet.values():
                    if ((tresor_type == 1 and isinstance(agent, MyAgentGold)) or 
                        (tresor_type == 2 and isinstance(agent, MyAgentStones))):
                        
                        available_agents.append(agent)  # Ajouter tous les agents du bon type
                        dist = agent.distance_to(x, y)
                        if dist < min_distance:
                            min_distance = dist
                            closest_agent = agent

                # ✅ Si un agent le plus proche est trouvé, lui envoyer en priorité
                if closest_agent:
                    print(f"📩 {self.id} envoie un message à {closest_agent.id} pour collecter à ({x}, {y})")
                    closest_agent.receive(self.id, ("collect", x, y, tresor_type))
                else:
                    print(f"⚠️ Aucun agent prioritaire disponible, envoi à tous les agents de type correspondant...")
                    for agent in available_agents:
                        print(f"📩 {self.id} envoie un message à {agent.id} pour collecter à ({x}, {y})")
                        agent.receive(self.id, ("collect", x, y, tresor_type))



        elif action == "collect":
            self.move_towards(x, y)

            if (self.posX, self.posY) == (x, y):
                if self.env.grilleTres[x][y] and self.env.grilleTres[x][y].getValue() > 0:  # ✅ Vérifier si le trésor est encore présent
                    amount = min(self.capacity - self.treasure, self.env.grilleTres[x][y].getValue())

                    if amount > 0:  # ✅ Vérifier si on peut collecter quelque chose
                        self.treasure += amount
                        self.env.grilleTres[x][y].reduceValue(amount)
                        print(f"💰 {self.id} a collecté {amount} unités de trésor.")

                        # ✅ Supprimer le trésor s'il est entièrement collecté
                        if self.env.grilleTres[x][y].getValue() == 0:
                            print(f"🗑️ Trésor à ({x}, {y}) entièrement collecté, suppression...")
                            self.env.grilleTres[x][y] = None  # Supprime le trésor de la grille

                        self.task_list.pop(0)  # Supprime la tâche de collecte

                        # ✅ Ajouter la tâche de dépôt seulement si l'agent a collecté quelque chose
                        self.task_list.append(("deposit", self.env.posUnload[0], self.env.posUnload[1]))
                    else:
                        print(f"❌ {self.id} n'a rien pu collecter, tâche ignorée.")
                        self.task_list.pop(0)  # Supprime la tâche inutile
                else:
                    print(f"⚠️ {self.id} arrive trop tard, le trésor à ({x}, {y}) a disparu.")
                    self.task_list.pop(0)  # Supprime la tâche si le trésor n'existe plus




        elif action == "deposit":
            self.move_towards(x, y)
            if (self.posX, self.posY) == (x, y):  # ✅ L'agent atteint le dépôt
                if self.treasure > 0:  # ✅ Vérifie qu'il a quelque chose à déposer
                    print(f"📦 {self.id} dépose {self.treasure} unités au dépôt.")
                    self.env.task_manager.update_score(self.id, self.treasure)
                    self.treasure = 0
                else:
                    print(f"❌ {self.id} n'a rien à déposer, action ignorée.")

                self.task_list.pop(0)  # ✅ Supprime la tâche "deposit"
            self.move_away_from_depot()  # ✅ Quitter immédiatement le dépôt



    def move_away_from_depot(self):
        """L'agent quitte la zone de dépôt après avoir déposé un trésor"""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        random.shuffle(directions)  # Mélanger les directions pour un déplacement naturel

        for dx, dy in directions:
            new_x, new_y = self.posX + dx, self.posY + dy
            if self.is_within_bounds(new_x, new_y) and not self.is_position_occupied(new_x, new_y):
                self.posX, self.posY = new_x, new_y
                print(f"🚶 {self.id} quitte la zone de dépôt vers ({new_x}, {new_y}).")
                return

    def is_position_occupied(self, x, y):
        """Vérifie si une position est occupée par un autre agent"""
        return any(agent.posX == x and agent.posY == y for agent in self.env.agentSet.values() if agent != self)


    def is_within_bounds(self, x, y):
        """Vérifie si une position est dans les limites de la grille"""
        return 0 <= x < self.env.tailleX and 0 <= y < self.env.tailleY



    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.getId() == self.getId()
        return False

    def move(self, x1, y1, x2, y2):
        """Fait bouger l'agent vers une case adjacente"""
        if x1 == self.posX and y1 == self.posY:
            if self.env.move(self, x1, y1, x2, y2):
                self.posX = x2
                self.posY = y2
                return 1
        return -1

    def getId(self):
        return self.id

    def getPos(self):
        return (self.posX, self.posY)

    def add_task(self, task):
        """Ajoute une tâche à l'agent et trie les tâches par distance"""
        self.task_list.append(task)
        self.task_list.sort(key=lambda t: self.distance_to(t[1], t[2]))

    def distance_to(self, x, y):
        """Calcule la distance Manhattan à une position donnée"""
        return abs(self.posX - x) + abs(self.posY - y)
   
    def can_collect(self, treasure_type):
        """Cette méthode sera redéfinie par les sous-classes"""
        return False

   


        


    def move_towards(self, target_x, target_y):
        if self.posX == target_x and self.posY == target_y:
            print(f"✅ {self.id} est arrivé à {target_x}, {target_y}")
            return  # L'agent est déjà à destination

        print(f"🚶 {self.id} se déplace vers {target_x}, {target_y}")

        if self.posX < target_x:
            self.posX += 1
        elif self.posX > target_x:
            self.posX -= 1
        if self.posY < target_y:
            self.posY += 1
        elif self.posY > target_y:
            self.posY -= 1



    def collect_treasure(self):
        x, y = self.posX, self.posY
        if self.env.grilleTres[x][y] and self.env.grilleTres[x][y].isOpen():
            amount = min(self.capacity - self.treasure, self.env.grilleTres[x][y].getValue())
            self.treasure += amount
            self.env.grilleTres[x][y].resetValue()
            print(f"{self.id} a collecté {amount} unités de trésor.")

            # ✅ Ajoute une tâche de dépôt après la collecte
            self.task_list.append(("deposit", self.env.posUnload[0], self.env.posUnload[1]))


    def send(self, idReceiver, textContent):
        """Envoie un message à un autre agent ou à tous les agents"""
        if idReceiver == "all":
            for agent in self.env.agentSet.values():
                if agent.getId() != self.id:
                    agent.receive(self.id, textContent)
        else:
            self.env.send(self.id, idReceiver, textContent)

    def receive(self, idReceiver, textContent):
        """Ajoute un message dans la boîte aux lettres"""
        self.mailBox.append((idReceiver, textContent))

    def process_messages(self):
        """Lit et traite les messages"""
        while self.mailBox:
            idSender, textContent = self.mailBox.pop(0)
            print(f"📩 {self.id} a reçu de {idSender}: {textContent}")

    def __str__(self):
        return f"{self.id} ({self.posX}, {self.posY})"