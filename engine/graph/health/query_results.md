# Query Results - Actual Data

Real outputs from the Blood Ledger graph database.

---

## DATABASE STATS

| Node Type | Count |
|-----------|-------|
| Narrative | 139 |
| Place | 87 |
| Character | 49 |
| Tension | 22 |
| Thing | 34 |

| Relationship | Count |
|--------------|-------|
| BELIEVES | 1,679 |
| CONNECTS | 113 |
| AT | 54 |
| LOCATED_AT | 24 |

---

## CHARACTER QUERIES

### Who is at York right now?
**Quality: 9/10** | **5 rows**

| Name | Type | Visible |
|------|------|---------|
| Thorkel | minor | 1.0 |
| Wulfstan | background | 1.0 |
| Archil | minor | 1.0 |
| Waltheof | major | 1.0 |
| Hugh FitzBaldric | major | 1.0 |

York has two major Norman/Saxon power players (Waltheof the conflicted Saxon earl, Hugh the Norman tax collector), plus resistance figure Archil and some locals. Tense mix.

---

### All living companions and their locations
**Quality: 10/10** | **1 row**

| Name | Location | Visible |
|------|----------|---------|
| Aldric | Thornwick | 1.0 |

Only one companion in the database: Aldric, stationed at the player's home village of Thornwick. The band is small.

---

### Characters hiding (present but not visible)
**Quality: 8/10** | **0 rows**

Nobody is currently hiding. No ambushes set, no spies lurking. The world is in open daylight mode.

---

### Characters who witnessed events firsthand
**Quality: 8/10** | **3 rows**

| Witness | What They Saw | Certainty |
|---------|---------------|-----------|
| Aldric | Aldric's Oath | 1.0 |
| Wulfric | Edmund's Betrayal | 1.0 |
| Wulfric | Thornwick Burns | 1.0 |

Only 3 witnessed events recorded. Aldric saw the oath sworn. Wulfric saw Edmund's betrayal and the burning of Thornwick. These are the reliable sources—everyone else is working from hearsay.

---

### Characters by flaw
**Quality: 6/10** | **11 rows**

| Name | Flaw | Approach |
|------|------|----------|
| Edith Swan-neck | wrath | direct |
| Judith of Lens | wrath | direct |
| Dunstan | wrath | impulsive |
| Ulfkil | doubt | direct |
| Picot of Cambridge | wrath | direct |
| Edgar Ætheling | doubt | direct |
| Morcar | wrath | deliberate |
| Edwin | pride | direct |
| Robert Cumin | wrath | impulsive |
| William | wrath | deliberate |
| Aldric | doubt | cautious |

**Wrath dominates** - 7 characters driven by anger (Cumin, William, Morcar, etc.). **Doubt** affects 3 (Edgar, Ulfkil, Aldric). **Pride** only Edwin. This is an angry world, full of people ready to lash out.

---

### Major characters and their locations
**Quality: 10/10** | **4 rows**

| Name | Type | Location |
|------|------|----------|
| Aldric | companion | Thornwick |
| Gospatric | major | Durham |
| Hugh FitzBaldric | major | York |
| Waltheof | major | York |

Power is concentrated: York holds both Norman tax collector Hugh and conflicted Saxon earl Waltheof. Gospatric sits in Durham. The companion Aldric waits at home.

---

## KNOWLEDGE & BELIEFS

### Who originated narratives?
**Quality: 9/10** | **12 rows**

| Originator | Narrative | Type |
|------------|-----------|------|
| Edith Swan-neck | Edith knows where Harold lies | secret |
| Aldric | Aldric's brother died at Stamford Bridge | memory |
| Aldric | Aldric's Oath | oath |
| Reinfrid | Reinfrid seeks penance | memory |
| Reinfrid | Whitby Refounded | memory |
| Æthelwine | St Cuthbert's Vigil | memory |
| Ealdred | York Burns | memory |
| Alan Rufus | Richmond Castle Begun | memory |
| William Malet | Malet buried Harold | secret |
| William Malet | Malet's Justice | memory |
| Gospatric | Gospatric paid William gold | secret |
| Robert Cumin | Cumin's Cruelty | reputation |

The secret-keepers: **Edith** knows where Harold is buried. **Malet** buried him. **Gospatric** knows how he bought his earldom. These are the people who created the narratives others now believe.

---

### Who knows the most? (Information brokers)
**Quality: 8/10** | **Top 10**

| Name | Type | Knowledge Count |
|------|------|-----------------|
| Waltheof | major | 63 |
| Dunstan | minor | 62 |
| Hild | background | 62 |
| Wulfstan | background | 61 |
| William Malet | major | 61 |
| Archil | minor | 61 |
| Thorkel | minor | 60 |
| Hugh FitzBaldric | major | 60 |
| Gospatric | major | 59 |
| Ealdred | major | 59 |

**Waltheof knows the most** (63 narratives)—makes sense, he straddles both worlds. Background characters like **Hild** and **Wulfstan** are surprisingly well-informed (servants hear everything). The major players (Malet, Hugh, Gospatric, Ealdred) all hover around 59-61.

---

### Narrative spread - who was told things
**Quality: 8/10** | **1,520 rows** (showing sample)

| Learned By | Narrative | Certainty |
|------------|-----------|-----------|
| Edith Swan-neck | Edith knows where Harold lies | 0.9 |
| Edith Swan-neck | Edgar is the rightful King | 0.7 |
| Judith of Lens | Judith reports to William | 0.9 |
| Judith of Lens | Ilbert de Lacy controls Otley | 0.5 |
| Judith of Lens | Alan Rufus controls Bedale | 0.5 |

Massive knowledge network—1,520 belief relationships. Most information spreads by being "told" rather than witnessed. This is a world of rumors and second-hand accounts.

---

## SECRETS

### Secrets in the database
**Quality: 10/10** | **4 rows**

| Secret | Content |
|--------|---------|
| Edith knows where Harold lies | Edith Swan-neck identified Harold's body and knows his true burial place. |
| Malet buried Harold | William Malet, though half-Norman, buried King Harold after Hastings. He knew Harold. |
| Gospatric paid William gold | Gospatric bought his earldom from William for a vast sum of gold. Some say it was treasure from Durham Cathedral. |
| Judith reports to William | Judith of Lens, Waltheof's Norman wife, sends letters to King William about her husband's activities. |

Four devastating secrets:
- **Harold's burial location** - whoever finds this controls a powerful symbol
- **Malet's divided loyalty** - he buried the enemy king
- **Gospatric's corruption** - he bought what he claims by right
- **Judith is a spy** - Waltheof's own wife betrays him

---

## RUMORS

### Rumors spreading
**Quality: 8/10** | **4 rows**

| Rumor | Content |
|-------|---------|
| The resistance is forming | Saxon thegns are meeting in secret. They plan to throw off the Norman yoke. |
| Edgar plots with Malcolm | Edgar Ætheling and King Malcolm are planning something. The Scots will march south. |
| The Danes are coming | King Sweyn of Denmark is preparing a fleet. He will come to claim England. |
| William returns to Normandy | The Bastard has gone back to Normandy. Now is the time to strike. |

Four active rumors—all about **hope for rebellion**: resistance forming, Edgar plotting, Danes coming, William absent. Whether true or not, these shape behavior.

---

## OATHS & BLOOD

### Oaths sworn
**Quality: 9/10** | **1 row**

| Oath | Content |
|------|---------|
| Aldric's Oath | Aldric swore to your father he would protect you. He's the only one who stayed. |

Only one formal oath in the database—Aldric's promise to the player's father. This is the core relationship bond.

---

### Blood feuds
**Quality: 9/10** | **1 row**

| Feud | Content | Type |
|------|---------|------|
| Edmund's Betrayal | Edmund sold the family to the Normans while father lay dying. He took the land, the title, everything. | blood |

One blood feud: Edmund's betrayal. This is the player's driving vendetta—a family member who sold them out.

---

## PLACES

### Place types
**Quality: 5/10** | **6 types**

| Type | Count |
|------|-------|
| village | 24 |
| town | 20 |
| abbey | 7 |
| hold | 5 |
| crossing | 3 |
| city | 3 |

62 places total. Mostly villages (24) and towns (20). 7 abbeys, 5 Norman castles, 3 river crossings, 3 cities (York, Durham, Lincoln).

---

### River crossings (strategic)
**Quality: 8/10** | **3 rows**

| Crossing |
|----------|
| Tees Crossing |
| Ouse Ford |
| Humber Crossing |

Three choke points: Tees (northern border), Ouse (near York), Humber (southern boundary). Control these to control movement.

---

### Norman strongholds
**Quality: 8/10** | **5 rows**

| Castle |
|--------|
| Helmsley Castle |
| Richmond Castle |
| Scarborough Castle |
| Durham Castle |
| York Castle |

Five Norman castles—the military occupation infrastructure. York and Durham are the key power centers; Richmond, Scarborough, Helmsley lock down the regions.

---

### Abbeys and monasteries
**Quality: 7/10** | **7 rows**

| Abbey | Type |
|-------|------|
| Ripon Minster | abbey |
| Selby Abbey | abbey |
| York Minster | abbey |
| Durham Cathedral | abbey |
| Rievaulx Abbey | abbey |
| Fountains Abbey | abbey |
| Whitby Abbey | abbey |

Seven religious houses. York Minster and Durham Cathedral are power centers; Whitby is being rebuilt by the penitent Reinfrid; Fountains and Rievaulx are wilderness retreats.

---

### Travel from York
**Quality: 9/10** | **10 connected places**

| Destination | Type |
|-------------|------|
| Easingwold | village |
| Sheriff Hutton | village |
| Crayke | village |
| Stamford Bridge | village |
| York Minster | abbey |
| Ouse Ford | crossing |
| York Castle | hold |
| Tadcaster | town |
| Selby | town |
| Malton | town |

From York you can reach: local villages (Easingwold, Sheriff Hutton, Crayke), the historic battlefield (Stamford Bridge), key towns (Tadcaster, Selby, Malton), and internal locations (Castle, Minster, Ford). Note: travel times not yet populated.

---

## TENSIONS

### All active tensions
**Quality: 10/10** | **17 rows** (showing top)

| Tension | Description | Pressure | Breaking |
|---------|-------------|----------|----------|
| tension_cumin_cruelty | Robert Cumin's cruelty builds a fire. Durham will burn before long. | **0.65** | 0.85 |
| tension_northern_rebellion | The North will rise against Norman rule. | **0.60** | 0.90 |
| tension_waltheof_oath | Waltheof swore to William but his heart is Saxon. How long can he serve two masters? | **0.55** | 0.90 |
| tension_york_whispers | York whispers of resistance. The Normans grow suspicious. | 0.50 | 0.80 |
| tension_aldric_revenge | Aldric's brother died fighting invaders. Now more invaders hold the land. | 0.50 | 0.90 |
| tension_aethelwine_resistance | Bishop Æthelwine guards Cuthbert's bones and dreams of Saxon freedom. | 0.50 | 0.85 |
| tension_danish_intervention | Sweyn of Denmark waits for the right moment. | 0.50 | 0.80 |
| tension_thornwick_taxes | The harvest was poor but the Normans still demand their share. | 0.45 | 0.80 |
| tension_scottish_raids | Malcolm of Scotland shelters the ætheling and eyes the North. | 0.45 | 0.85 |
| tension_reinfrid_guilt | Can rebuilding an abbey atone for the blood at Hastings? | 0.40 | 0.95 |

**Cumin's cruelty is closest to breaking** (0.65/0.85 = 76%). The **northern rebellion** (0.60/0.90 = 67%) and **Waltheof's conflict** (0.55/0.90 = 61%) follow close behind. Multiple tensions at 0.50—the North is a powder keg.

---

### Tensions near breaking (>0.5 pressure)
**Quality: 10/10** | **3 rows**

| Tension | Pressure | Breaking Point |
|---------|----------|----------------|
| tension_cumin_cruelty | 0.65 | 0.85 |
| tension_northern_rebellion | 0.60 | 0.90 |
| tension_waltheof_oath | 0.55 | 0.90 |

Three imminent crises:
1. **Cumin's cruelty** → Durham uprising
2. **Northern rebellion** → Coordinated resistance
3. **Waltheof's oath** → His loyalty will break one way or another

---

## COMPLEX QUERIES

### Characters at same location (potential confrontations)
**Quality: 10/10** | **11 pairs**

**York (5 characters, 10 pairs):**
- Thorkel + Wulfstan
- Thorkel + Archil
- Thorkel + Waltheof
- Thorkel + Hugh FitzBaldric
- Wulfstan + Archil
- Wulfstan + Waltheof
- Wulfstan + Hugh FitzBaldric
- Archil + Waltheof
- Archil + Hugh FitzBaldric
- **Waltheof + Hugh FitzBaldric** ← Saxon earl meets Norman tax collector

**Durham (2 characters, 1 pair):**
- **Ligulf + Gospatric** ← Two Saxon power players

York is crowded and tense. The Waltheof/Hugh pairing is especially volatile—the conflicted Saxon earl facing the brutal Norman administrator.

---

## THINGS

### All items in database
**Quality: 9/10** | **34 rows**

| Significance | Type | Item |
|--------------|------|------|
| legendary | relic | Bones of St. Cuthbert |
| legendary | weapon | Sword of Harold Godwinson |
| sacred | relic | St. Cuthbert's Gospel |
| sacred | relic | Shrine of St. Hild |
| sacred | relic | Ripon Gospels |
| sacred | token | Archbishop's Pectoral Cross |
| sacred | token | Keys to Durham Cathedral |
| sacred | treasure | Treasures of York Minster |
| sacred | treasure | Beverley Silver |
| political | document | Selby Abbey Charter |
| political | document | Royal Writ for Yorkshire |
| political | document | Charter of the Bishop's Peace |
| political | document | Norman Safe Conduct |
| political | document | Yorkshire Tax Rolls |
| political | letter | Sealed Letter |
| political | token | Sheriff's Seal of York |
| political | token | Earl's Seal of Durham |
| political | token | Keys to York Castle |
| political | token | Royal Messenger's Pouch |
| political | treasure | Tax Silver |
| political | treasure | Richmond Treasury |
| political | provisions | Norman Warhorses |
| personal | document | Thornwick Land Deed |
| personal | token | Father's Ring |
| personal | token | Waltheof's Ring |
| personal | treasure | Gospatric's Gold |
| personal | weapon | Breton Blade |
| personal | weapon | Huscarl's Axe |
| personal | weapon | Reinfrid's Buried Sword |
| mundane | armor | Norman Mail |
| mundane | weapon | Castle Armory |
| mundane | provisions | York Grain Stores |
| mundane | provisions | Salt from the Coast |
| mundane | provisions | Monastery Herbs |

---

### Legendary Items
**Quality: 10/10** | **2 rows**

| Item | Location | Carried By |
|------|----------|------------|
| Bones of St. Cuthbert | Durham Cathedral | no one |
| Sword of Harold Godwinson | **unknown** | no one |

The two most powerful items in the game: St. Cuthbert's bones (religious power, guarded at Durham) and Harold's sword (legitimacy symbol, location lost). Finding the sword is a major quest.

---

### Sacred Relics and Locations
**Quality: 9/10** | **7 rows**

| Relic | Location |
|-------|----------|
| St. Cuthbert's Gospel | Durham Cathedral |
| Shrine of St. Hild | Whitby Abbey |
| Treasures of York Minster | York Minster |
| Ripon Gospels | Ripon Minster |
| Beverley Silver | Beverley |
| Archbishop's Pectoral Cross | *(carried)* |
| Keys to Durham Cathedral | *(carried)* |

Sacred items distributed across the abbeys. The cross and keys are personal items (carried by Ealdred and Æthelwine respectively).

---

### Hidden Treasures
**Quality: 9/10** | **3 rows**

| Treasure | Hidden At | Specific Location |
|----------|-----------|-------------------|
| Sealed Letter | York | Changes location. Currently in the Shambles. |
| Gospatric's Gold | Hexham | Buried beneath the old Roman stones, north of the abbey |
| Reinfrid's Buried Sword | Whitby Abbey | Buried beneath the chapter house floor |

Three hidden things: the resistance letter (moves around York), Gospatric's buried treasure (insurance policy at Hexham), and Reinfrid's sword (buried with his guilt at Whitby).

---

## NARRATIVE TYPES

### Breakdown by type
**Quality: 5/10** | **9 types**

| Type | Count |
|------|-------|
| control | 37 |
| memory | 25 |
| rumour | 4 |
| claim | 4 |
| secret | 4 |
| debt | 3 |
| blood | 1 |
| oath | 1 |
| reputation | 1 |

**Control narratives dominate** (37)—who controls what territory. **Memories** are second (25)—personal histories. Then rumors, claims, secrets (4 each), debts (3). Only 1 each of blood, oath, reputation. The world is defined by territorial control and personal memory.
