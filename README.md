# turtle_scanner_josue
## Installation

### 1. Créer le workspace ROS

```sh
mkdir -p ~/turtle_ws/src
cd ~/turtle_ws
colcon build
```

### 2. Cloner les dépôts

```sh
cd src
git clone git@github.com:njaraT/turtle_scanner_josue.git
```

### 3. Build & source

```sh
cd ..
colcon build
source install/setup.bash
```

## Partie 1

### Build

```bash
cd ~/ros2_ws
colcon build --packages-select turtle_scanner_josue
source install/setup.bash
```

### Lancement

Terminal 1 :

```bash
ros2 run turtlesim turtlesim_node
```

Terminal 2 :

```bash
source ~/ros2_ws/install/setup.bash
ros2 run turtle_scanner_josue spawn_target_node
```

### Resultat attendu

Une deuxieme tortue apparait dans TurtleSim avec le nom `turtle_target`, et le noeud affiche un
message contenant ses coordonnees.