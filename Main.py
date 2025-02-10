
import pygame
from Environment import Environment
from MyAgentGold import MyAgentGold
from MyAgentStones import MyAgentStones
from MyAgentChest import MyAgentChest
from Treasure import Treasure
from TaskManager import TaskManager




# --- CONSTANTES ---
TAILLE_GRILLE = 12
RECT_SIZE = 50
FPS = 2


COULEURS = {
    "fond": (255, 255, 255),  # Fond blanc
    "grille": (200, 200, 200),  # Gris clair pour la grille
    "agent_or": (255, 140, 0),  # Orange foncé
    "agent_pierres": (138, 43, 226),  # Violet
    "agent_coffre": (30, 144, 255),  # Bleu
    "depot": (34, 139, 34),  # Vert pour dépôt
    "tresor_or": (255, 215, 0),  # Jaune or
    "tresor_pierres": (0, 206, 209)  # Cyan
}

# Fonction d'affichage amélioré
def render_env(screen, env, agents, score):
    screen.fill(COULEURS["fond"])  # Remplir le fond

    #  Dessiner la grille
    for x in range(TAILLE_GRILLE):
        for y in range(TAILLE_GRILLE):
            pygame.draw.rect(screen, COULEURS["grille"], (x * RECT_SIZE, y * RECT_SIZE, RECT_SIZE, RECT_SIZE), 1)

    #  Afficher le dépôt en **VERT**
    depot_x, depot_y = env.posUnload
    font = pygame.font.Font(None, 36) 
    pygame.draw.rect(screen, COULEURS["depot"], (depot_x * RECT_SIZE, depot_y * RECT_SIZE, RECT_SIZE, RECT_SIZE))
    # Rendu du texte "D"
    text = font.render("D", True, (0, 0, 0))  # Texte noir
    text_rect = text.get_rect(center=(depot_x * RECT_SIZE + RECT_SIZE // 2, depot_y * RECT_SIZE + RECT_SIZE // 2))

    # Affichage du texte à l'écran
    screen.blit(text, text_rect)
    #  Afficher les trésors avec **arrondi**
    for x in range(TAILLE_GRILLE):
        for y in range(TAILLE_GRILLE):
            if env.grilleTres[x][y]:
                couleur = COULEURS["tresor_or"] if env.grilleTres[x][y].getType() == 1 else COULEURS["tresor_pierres"]
                pygame.draw.rect(screen, couleur, (x * RECT_SIZE + 5, y * RECT_SIZE + 5, RECT_SIZE - 10, RECT_SIZE - 10), border_radius=10)

    # 🕵️ Afficher les agents avec **contour blanc**
    for agent in agents.values():
        posX, posY = agent.getPos()
        couleur = (COULEURS["agent_or"] if isinstance(agent, MyAgentGold)
                   else COULEURS["agent_pierres"] if isinstance(agent, MyAgentStones)
                   else COULEURS["agent_coffre"])
        
        pygame.draw.circle(screen, (0, 0, 0), (posX * RECT_SIZE + RECT_SIZE // 2, posY * RECT_SIZE + RECT_SIZE // 2), RECT_SIZE // 3 + 3)  # Contour blanc
        pygame.draw.circle(screen, couleur, (posX * RECT_SIZE + RECT_SIZE // 2, posY * RECT_SIZE + RECT_SIZE // 2), RECT_SIZE // 3)

    # 🏆 Affichage **grand et centré** du score
    font = pygame.font.Font(None, 50)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()  # Mettre à jour l'affichage


                        

def loadFileConfig(nameFile):
    """Charge la configuration des agents et trésors depuis env1.txt"""
    with open(nameFile) as file:
        lines = file.readlines()
    
    tailleX, tailleY = map(int, lines[1].split())
    cPosDepot = tuple(map(int, lines[3].split()))
    dictAgent = {}
    env = Environment(tailleX, tailleY, cPosDepot)
    cpt = 0

    for ligne in lines[4:]:
        ligneSplit = ligne.strip().split(":")
        if ligneSplit[0] == "tres":
            tresor_type = 1 if ligneSplit[1] == "or" else 2
            env.addTreasure(Treasure(tresor_type, int(ligneSplit[4])), int(ligneSplit[2]), int(ligneSplit[3]))
        elif ligneSplit[0] == "AG":
            id = f"agent{cpt}"
            posX, posY = int(ligneSplit[2]), int(ligneSplit[3])
            capacite = int(ligneSplit[4]) if len(ligneSplit) > 4 else 0

            if ligneSplit[1] == "or":
                agent = MyAgentGold(id, posX, posY, capacite, env)
            elif ligneSplit[1] == "pierres":
                agent = MyAgentStones(id, posX, posY, capacite, env)
            else:
                agent = MyAgentChest(id, posX, posY, env, capacity=0)
            
            dictAgent[id] = agent
            env.addAgent(agent)
            cpt += 1
    
    env.addAgentSet(dictAgent)
    return env, dictAgent

#  Fonction principale
def main():
    env, agents = loadFileConfig("env2.txt")
    task_manager = TaskManager(env)
    env.task_manager = task_manager  # Lien avec les agents

    pygame.init()
    screen = pygame.display.set_mode((TAILLE_GRILLE * RECT_SIZE, TAILLE_GRILLE * RECT_SIZE))
    pygame.display.set_caption("Gestion des Trésors")  #  Titre de la fenêtre

    running = True
    clock = pygame.time.Clock()
    iteration = 0

    while running:
        if iteration % 10 == 0:  #  Générer un trésor toutes les 10 itérations
            env.gen_new_treasures(1, 10)
            print("🎁 Nouveau trésor généré !")

        task_manager.detect_new_tasks()
        task_manager.assign_tasks(agents)

        for agent in agents.values():
            agent.execute_task()
            agent.process_messages()

        render_env(screen, env, agents, task_manager.score_global)  #  Mettre à jour l'affichage

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(FPS)
        iteration += 1

    pygame.quit()

if __name__ == "__main__":
    main()
