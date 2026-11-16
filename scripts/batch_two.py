"""Original authored expansion, batch 2. Upserts stable records without deleting progress IDs.
Chapter texts and answers are original; references identify learning scope, not copied prose.
"""
import json,pathlib,copy
ROOT=pathlib.Path(__file__).resolve().parents[1]
chapters=[]
def add(sid,form,slug,title,refs,paragraphs,examples,terms,questions,objectives):
 assert len(questions)==15,(slug,len(questions))
 chapters.append(dict(subjectId=sid,form=form,slug=slug,title=title,refs=refs,paragraphs=paragraphs,examples=examples,terms=terms,questions=questions,objectives=objectives))
# A question is (prompt, model answer, feedback); optional fourth entry lists MCQ options.
add('chemistry',1,'elements','Elements, compounds and the periodic table',[4,5,6],[
'An element contains only one kind of atom. Copper wire, oxygen gas and a piece of pure carbon are examples. Some elements occur as single atoms, while others occur as molecules: O₂ has two oxygen atoms joined together. An element is therefore not the same thing as a single atom. A compound contains atoms of different elements chemically joined in a fixed ratio. Water is a compound because each H₂O molecule contains two hydrogen atoms for every oxygen atom.',
'A chemical symbol identifies an element. The first letter is capital and a second letter, if present, is lower case: C is carbon, Ca calcium, Co cobalt and Cl chlorine. A formula identifies the kinds and relative numbers of atoms in a substance. CO₂ has one carbon atom and two oxygen atoms per molecule. The small lower number is a subscript; a number written before a formula counts complete units. Thus 2H₂O contains four hydrogen atoms and two oxygen atoms altogether.',
'In a compound the properties can differ greatly from those of its elements. Hydrogen is a combustible gas and oxygen supports combustion, but water is a liquid at ordinary room conditions and can extinguish some fires. This comparison does not mean water is safe for every fire: never use water on live electrical equipment or burning cooking oil. Separating a compound into its elements requires chemical change; a mixture can usually be separated using physical differences.',
'The periodic table orders elements by atomic number. Its horizontal rows are periods and its vertical columns are groups. For the first twenty elements the order is H, He, Li, Be, B, C, N, O, F, Ne, Na, Mg, Al, Si, P, S, Cl, Ar, K, Ca. Most metals are on the left and centre; most non-metals are towards the right. Metals generally conduct electricity well, are malleable and form positive ions, but statements about materials need exceptions: graphite, a form of carbon, conducts electricity although carbon is a non-metal.'],[
'Count atoms in CO₂: C has no subscript, so it contributes 1 atom; O has subscript 2, so there are 2 oxygen atoms. Total = 3 atoms per molecule.',
'Classify air and pure water: air is a mixture with variable proportions of gases; pure water is a compound with a fixed hydrogen-to-oxygen ratio of 2:1.',
'Interpret 3MgO: each formula unit contains 1 magnesium and 1 oxygen atom. Three units contain 3 magnesium and 3 oxygen atoms. The coefficient multiplies the whole formula.'],
{'element':'A substance containing only one kind of atom.','compound':'A substance whose different elements are chemically joined in a fixed ratio.','period':'A horizontal row in the periodic table.'},[
('What is an element?','A substance containing only one kind of atom.','The definition concerns atom type, not the number of atoms.'),
('Which is a compound?','Water','Water contains chemically joined hydrogen and oxygen.',['Water','Copper','Oxygen']),
('Write the symbol for sodium.','Na','The N is capital and a is lower case.'),
('Name the element represented by Ca.','Calcium','Ca is different from C, which is carbon.'),
('How many oxygen atoms are in one CO₂ molecule?','2','The subscript 2 applies to oxygen.'),
('Count all atoms in one H₂O molecule.','3: two hydrogen and one oxygen.','Add both element counts.'),
('Count hydrogen atoms in 2H₂O.','4','The coefficient 2 multiplies the subscript 2.'),
('What does a horizontal row of the periodic table represent?','A period.','Groups are vertical columns.'),
('What is the first element in the periodic table?','Hydrogen','The table starts with atomic number 1.'),
('Name one conducting non-metal mentioned in the chapter.','Graphite, a form of carbon.','This is an exception to a simple metal/non-metal rule.'),
('Explain one difference between a mixture and a compound.','A mixture has physically combined components and variable composition; a compound has chemically joined elements in a fixed ratio.','Give a linked comparison, not just two examples.'),
('Why is oxygen gas O₂ still an element?','Both atoms are oxygen atoms, so only one kind of atom is present.','Two atoms do not imply two different elements.'),
('List the elements with symbols Mg, Al and Si.','Magnesium, aluminium and silicon.','Order and symbol recognition are both important.'),
('Can ordinary filtration separate pure water into hydrogen and oxygen?','No. That separation requires a chemical change.','Filtration separates physical components of mixtures.'),
('Explain why the properties of water cannot be predicted simply by adding the properties of hydrogen and oxygen.','Chemical joining produces a different substance whose properties differ from those of its constituent elements.','Use the gas-to-liquid comparison as evidence.')],['Distinguish elements, compounds and mixtures.','Read symbols and simple formulae.','Identify periods, groups and the first twenty elements.'])
add('chemistry',2,'atoms','Atomic structure and electron arrangements',[1,2,3,11],[
'An atom has a small, dense nucleus containing positively charged protons and uncharged neutrons. Negatively charged electrons occupy regions around the nucleus. Most of the atomic volume is outside the nucleus. The shell diagrams used in this chapter are useful models for counting electrons; they are not photographs of tiny balls following fixed circular paths.',
'The atomic number Z is the number of protons. It identifies the element. The mass number A is the total number of protons and neutrons in a particular atom, so neutron number = A − Z. A neutral atom has equal numbers of protons and electrons. An ion forms when electrons are lost or gained; ordinary ion formation does not change the number of protons in the nucleus.',
'For introductory arrangements of the first twenty elements, fill the first shell with up to 2 electrons, then the second with up to 8, and use the school-level arrangements 2,8,8,1 for potassium and 2,8,8,2 for calcium. Sodium has 11 electrons arranged 2,8,1. Chlorine has 17 arranged 2,8,7. These simple shell counts describe the first twenty elements and should not be extended as a universal rule for all elements.',
'Atoms of the same element can have different neutron numbers: these are isotopes. Carbon-12 and carbon-14 both have six protons but have six and eight neutrons respectively. Their shared proton number makes them carbon. Electron arrangements connect to the periodic table: the occupied-shell count gives the period for these elements. Atoms in groups 1 and 2 have one and two outer electrons; groups 13–18 usually have three to eight outer electrons, with helium an exception having two.'],[
'For sodium-23, Z = 11 and A = 23. Protons = 11; neutrons = 23 − 11 = 12; a neutral atom has 11 electrons, arranged 2,8,1.',
'An oxygen atom has Z = 8 and A = 16. It has 8 protons, 8 neutrons and 8 electrons. If it gains two electrons to form O²⁻, it has 10 electrons but still 8 protons.',
'Calcium has arrangement 2,8,8,2. Four occupied shells place it in period 4, and two outer electrons place it in group 2.'],
{'atomic number':'The number of protons in an atomic nucleus.','isotopes':'Atoms of one element with different neutron numbers.','ion':'An atom or group with a net electric charge.'},[
('Which particle has a positive charge?','Proton','Electrons are negative and neutrons uncharged.',['Proton','Electron','Neutron']),
('Define mass number.','The total number of protons and neutrons in an atom.','Do not include electrons.'),
('An atom has 12 protons. What is its atomic number?','12','Atomic number equals proton number.'),
('An atom has A = 24 and Z = 12. Find its neutrons.','12','24 − 12 = 12.'),
('How many electrons are in a neutral nitrogen atom with Z = 7?','7','Neutral atoms have equal proton and electron numbers.'),
('Write the electron arrangement of sodium with Z = 11.','2,8,1','The shell counts add to 11.'),
('Write the electron arrangement of magnesium with Z = 12.','2,8,2','The shell counts add to 12.'),
('What changes when an atom forms a positive ion?','It loses one or more electrons.','Losing negative charge leaves a net positive charge.'),
('An atom has 17 protons and 18 electrons. State its charge.','−1','There is one more negative charge than positive charge.'),
('What do isotopes of an element have in common?','The same number of protons.','Different proton numbers would mean different elements.'),
('Find the neutrons in carbon-14 with Z = 6.','8','14 − 6 = 8.'),
('An atom has arrangement 2,8,7. State its period.','3','There are three occupied shells.'),
('How many outer electrons does neutral calcium have?','2','Its arrangement is 2,8,8,2.'),
('Explain why changing neutron number does not change the element.','The element is identified by its proton number, which remains unchanged.','Link identity to atomic number.'),
('Distinguish an isotope from an ion.','Isotopes differ in neutron number; an ion has a net charge due to electron gain or loss.','Both differences must be clear.')],['Calculate proton, neutron and electron numbers.','Use first-twenty shell arrangements.','Relate arrangements to period and group.'])
add('physics',1,'forces','Force, pressure, work and energy',[5,10,11],[
'A force is a push or pull measured in newtons (N). It can change an object’s motion or shape. Several forces may act together: the resultant is their combined effect, taking direction into account. Two opposite forces of 8 N and 3 N have a resultant of 5 N towards the larger force. Balanced forces give zero resultant; this can occur while an object is at rest or moving at constant velocity.',
'Pressure is normal force per unit area: p = F/A. Its SI unit is the pascal, equivalent to N/m². A smaller contact area produces more pressure for the same force. A sharp blade therefore cuts more readily than a blunt one. In a stationary liquid, pressure increases with depth; liquid pressure acts in all directions at a point. When using p = ρgh for pressure due to a liquid, use density in kg/m³ and depth in metres.',
'Work is done when a force causes displacement in its direction. For a constant force parallel to motion, W = Fs, in joules (J). Holding a heavy bag stationary may feel tiring, but the simple mechanical work on the bag is zero because it has no displacement. Energy is the capacity to do work and can be transferred between stores or pathways. Near Earth, gravitational potential energy gained = mgh.',
'Power is the rate of doing work or transferring energy: P = W/t, measured in watts (W). A machine doing 600 J of useful work in 3 s has useful power 200 W. Efficiency compares useful output with total input: useful energy output/input energy × 100%. Energy is conserved, but not all input becomes the intended useful output; some usually warms the surroundings. Always state which output is considered useful.'],[
'A 120 N force acts normally on 0.04 m². Pressure = 120/0.04 = 3000 Pa. If the area doubles with the same force, pressure halves to 1500 Pa.',
'A horizontal force of 25 N moves a box 4 m along the force. Work = 25 × 4 = 100 J. If this takes 5 s, average power = 100/5 = 20 W.',
'Raise a 3 kg load through 2 m. Using g = 10 N/kg, potential energy gain = 3 × 10 × 2 = 60 J. If input energy is 100 J, efficiency = 60/100 × 100% = 60%.'],
{'resultant':'The combined effect of forces, accounting for their directions.','pressure':'Normal force acting per unit area.','power':'Work done or energy transferred per unit time.'},[
('State the SI unit of force.','Newton (N).','Do not confuse mass in kg with force in N.'),
('Opposite forces are 12 N east and 7 N west. Find the resultant.','5 N east.','Subtract magnitudes and keep the larger-force direction.'),
('Does zero resultant always mean an object is stationary?','No; it can move at constant velocity.','A change of velocity requires resultant force.'),
('Calculate pressure for 80 N on 0.02 m².','4000 Pa','p = 80/0.02.'),
('What happens to pressure if area doubles for the same normal force?','It halves.','Pressure is inversely proportional to area.'),
('Find work done by 15 N over 6 m in its direction.','90 J','W = 15 × 6.'),
('Find power when 240 J is transferred in 12 s.','20 W','P = 240/12.'),
('Calculate potential energy gained by 5 kg raised 3 m; g = 10 N/kg.','150 J','mgh = 5 × 10 × 3.'),
('Input is 500 J and useful output 350 J. Find efficiency.','70%','350/500 × 100%.'),
('What is the mechanical work on a stationary held bag?','Zero in the simple W = Fs model.','The bag has no displacement.'),
('Why does a sharp knife produce greater pressure for the same force?','Its smaller contact area increases force per unit area.','Mention both area and pressure.'),
('Name the unit equivalent to one pascal.','1 N/m²','Pressure is force divided by area.'),
('Calculate liquid pressure for ρ = 1000 kg/m³, h = 2 m, g = 10 N/kg.','20,000 Pa','ρgh = 1000 × 10 × 2.'),
('Distinguish work from power.','Work is an energy transfer by force through displacement; power is the rate of transferring energy.','Give the time distinction.'),
('Why can efficiency be below 100% although energy is conserved?','Some input energy is transferred in forms that are not the intended useful output, such as heating the surroundings.','Energy is not destroyed.')],['Calculate pressure, work, power and efficiency.','Distinguish force balance from being at rest.','Use units consistently.'])
add('physics',2,'light','Light, reflection and refraction',[1,5,6],[
'A luminous object emits its own light; a non-luminous object is seen when light reaches it and is reflected towards the eye. In a uniform transparent medium, light travels approximately in straight lines. A ray is a line used to show the direction of travel. Transparent materials transmit light with clear images, translucent materials transmit scattered light, and opaque materials prevent most light from passing through.',
'Reflection occurs when light returns from a surface. Draw a normal perpendicular to the surface at the point where the ray meets it. The angle of incidence and angle of reflection are measured between the rays and this normal, not the surface. The laws of reflection state that these angles are equal and that the incident ray, reflected ray and normal lie in one plane. Smooth surfaces give regular reflection; rough surfaces scatter reflected rays because their local normals differ.',
'A plane mirror forms an upright, virtual image of the same size as the object. The image is as far behind the mirror as the object is in front. A virtual image cannot be projected directly onto a screen: the rays only appear to come from behind the mirror. Lateral inversion describes reversal across the mirror’s perpendicular direction; use diagrams to reason rather than treating it as a literal exchange of every left and right direction.',
'Refraction is a change in direction associated with a change of speed when light crosses obliquely between media. Entering glass from air, a ray usually bends towards the normal; leaving glass for air, it bends away. At normal incidence it changes speed without bending. A convex lens can converge parallel rays to a focus. For a converging lens, an object beyond the focal length can form a real image; an object inside the focal length produces a virtual magnified image. Never look at the Sun through a lens or focus sunlight near eyes or flammable materials.'],[
'An incident ray makes 35° with the normal. The reflected ray also makes 35° with the normal. The angle between the incident and reflected rays is 70°.',
'An object is 12 cm in front of a plane mirror. Its image is 12 cm behind it, so the object–image separation is 24 cm.',
'A ray makes 30° with a flat mirror surface. Its angle to the normal is 90° − 30° = 60°, so the angle of reflection is 60°.'],
{'normal':'A line perpendicular to a surface at the point of incidence.','refraction':'Change in a ray’s direction when its speed changes across a boundary at oblique incidence.','virtual image':'An image formed where rays appear to originate, rather than actually meet.'},[
('Give an example of a luminous object.','A lit lamp or the Sun.','It emits its own light.'),
('What is a normal in a ray diagram?','A line perpendicular to the surface at the point of incidence.','It is a construction line, not a travelling ray.'),
('Incidence angle is 42°. Find reflection angle.','42°','Angles are measured to the normal.'),
('A ray makes 20° with a mirror surface. Find its incidence angle.','70°','90° − 20°.'),
('An object is 8 cm before a plane mirror. How far is its image behind?','8 cm','Plane-mirror distances are equal.'),
('For that object, find the object–image separation.','16 cm','Add 8 cm in front and 8 cm behind.'),
('State two plane-mirror image properties.','Upright and virtual; same size is also valid.','Give any two correct properties.'),
('Can a plane-mirror image be projected directly on a screen?','No, it is virtual.','The rays do not actually converge at the image.'),
('What type of lens can converge parallel light rays?','Convex/converging lens.','Parallel rays meet near its principal focus.'),
('What happens to an oblique ray entering glass from air?','It normally bends towards the normal.','Its speed decreases in glass.'),
('Does a ray bend at normal incidence?','No, although its speed can change.','A change of speed need not produce a change of direction.'),
('Why can we see a book that does not emit light?','It reflects light into our eyes.','Both incident light and a path to the eye are needed.'),
('Distinguish transparent and translucent materials.','Transparent materials transmit clear images; translucent materials scatter transmitted light so images are not clear.','Both can transmit some light.'),
('Why do rough surfaces scatter reflected light?','The surface has different local normals, so reflected rays travel in different directions.','The law of reflection still applies locally.'),
('State one essential lens safety rule.','Never look at the Sun through a lens or focus its light near eyes.','Concentrated light can cause injury.')],['Draw normals and apply reflection angles.','Describe plane-mirror images.','Explain refraction and basic lens action.'])
add('biology',1,'photosynthesis','Photosynthesis and leaf structure',[3,8,9],[
'Photosynthesis is the process by which green plants use light energy to make organic food from carbon dioxide and water. Chlorophyll in chloroplasts absorbs light. A school-level word equation is carbon dioxide + water → glucose + oxygen, with light and chlorophyll as conditions. Glucose is a starting material for other substances; it can be used in respiration, converted to starch for storage or used to make cellulose. Plants do not obtain their main food supply by absorbing ready-made food from soil.',
'A leaf’s broad surface intercepts light, while its thin shape keeps diffusion distances short. The upper epidermis and cuticle protect it while allowing light through. Palisade cells commonly have many chloroplasts. Spongy mesophyll contains air spaces that help gas movement. Stomata are pores controlled by guard cells; they allow gas exchange but also permit water vapour to escape. Veins supply water through xylem and carry sugars through phloem.',
'Water is taken up by roots and carbon dioxide enters mainly through stomata. Light intensity, carbon dioxide availability and temperature can limit photosynthesis. Increasing one factor will not keep increasing the rate if a different factor has become limiting. Mineral ions are needed for healthy growth: magnesium contributes to chlorophyll and nitrates help plants make amino acids and proteins. A mineral deficiency is not the same as a lack of light.',
'An investigation should change one factor while keeping other important conditions similar. For a school starch test, a teacher removes leaf chlorophyll using hot ethanol in a water bath, then applies iodine solution; a blue-black colour indicates starch. Ethanol is flammable and must not be heated over a flame. This procedure requires teacher supervision, eye protection and appropriate handling of hot liquids. A paper-based interpretation of observations can be completed independently; do not perform this chemical test unsupervised.'],[
'A leaf kept in darkness has little opportunity to make new food by photosynthesis. Comparing it with an otherwise similar illuminated leaf helps investigate the need for light, provided stored starch has been considered.',
'In a variegated-leaf starch investigation, the green regions may test blue-black while non-green regions do not. Under controlled conditions this supports the role of chlorophyll; record the original pattern before removing the colour.',
'If a plant has adequate light but little carbon dioxide, adding more light may not increase its photosynthesis rate. Carbon dioxide is then a limiting factor.'],
{'photosynthesis':'Light-driven production of organic food from carbon dioxide and water.','stoma':'A leaf pore through which gases and water vapour can move.','limiting factor':'A condition whose shortage restricts a process even when other conditions are sufficient.'},[
('Name the gas used as a raw material in photosynthesis.','Carbon dioxide.','Oxygen is a product, not the carbon source.'),
('Which pigment absorbs light for photosynthesis?','Chlorophyll','It occurs in chloroplasts.'),
('Write the word equation for photosynthesis.','Carbon dioxide + water → glucose + oxygen, using light and chlorophyll.','Include both reactants and products.'),
('Where is water mainly taken into a flowering plant?','Through its roots.','Water then moves towards leaves through xylem.'),
('What tissue carries water in a leaf vein?','Xylem','Phloem transports sugars and other organic substances.'),
('State one advantage of a broad leaf.','It presents a large surface for intercepting light.','Relate the structure to photosynthesis.'),
('What are guard cells associated with?','Opening and closing stomata.','Stomata regulate gas exchange and water loss.'),
('Name the food-storage substance detected by iodine in a leaf.','Starch','A blue-black colour is a positive starch result.'),
('Why should ethanol not be heated directly over a flame?','It is flammable.','The starch test needs supervised safe heating.'),
('What is the role of magnesium in plants?','It is needed as part of chlorophyll.','A shortage can impair green pigment production.'),
('Why are nitrates important for plant growth?','They supply nitrogen for making amino acids and proteins.','They do not supply ready-made food.'),
('Define a limiting factor using carbon dioxide as an example.','Low carbon dioxide can restrict photosynthesis even when light and water are adequate.','Identify the restricting condition.'),
('State two ways a leaf is adapted for gas exchange.','It is thin and has stomata and internal air spaces.','Give two features linked to short/easy gas movement.'),
('What should remain similar in a test of light and photosynthesis?','Plant type, water, carbon dioxide, temperature and time, as far as practical.','Change light while controlling relevant alternatives.'),
('Describe how to report a plant investigation.','State the question, method, controlled conditions, observations, results, conclusion and limitations.','Separate observed facts from conclusions.')],['Explain food production in green plants.','Relate leaf structures to their functions.','Interpret supervised starch-test evidence safely.'])
add('biology',2,'nutrition','Human nutrition and digestion',[1,6,10],[
'A balanced diet supplies adequate nutrients in suitable proportions for a person’s needs. Carbohydrates and fats can supply energy; proteins provide amino acids for growth and repair. Vitamins and minerals support body processes. Water is essential for transport and chemical reactions, and dietary fibre helps normal bowel movement. Energy requirements vary with age, activity and other circumstances, so a single menu is not automatically suitable for everyone.',
'Digestion breaks large, insoluble food molecules into smaller molecules that can be absorbed. Mechanical digestion, such as chewing, breaks food into smaller pieces without changing their chemical identity. Chemical digestion uses enzymes, which are biological catalysts. In the mouth, teeth break food up and saliva helps swallowing; salivary amylase begins the digestion of starch. Food moves through the oesophagus by coordinated muscle contractions called peristalsis.',
'The stomach churns food and provides acidic conditions in which a protease begins protein digestion. Most digestion and nutrient absorption occur in the small intestine. The pancreas supplies digestive enzymes; bile is made by the liver, stored in the gall bladder and released into the small intestine. Bile emulsifies fats into small droplets and helps neutralise acid, but is not an enzyme. Lipase breaks fats down chemically.',
'The small intestine has folds and villi that provide a large absorptive surface. Villi have thin surfaces and a good blood supply, helping nutrients move away after absorption. The large intestine absorbs water and forms faeces from remaining material. Egestion removes undigested food; excretion removes metabolic waste, so they are different processes. A ruminant such as a cow has a multi-compartment stomach, and microbes help digest cellulose; humans do not have the same cellulose-digesting system.',
'Food-test observations support conclusions only when methods and controls are appropriate. Iodine can test starch; Benedict’s test can test reducing sugars with supervised heating; the biuret test can test protein. Chemical reagents are not food and must never be tasted. These tests require a teacher and laboratory precautions. For independent study, interpret supplied result tables and explain what the results support rather than attempting unsupervised chemical testing.'],[
'A sample turns blue-black with iodine. This supports the presence of starch. It does not by itself establish that the sample contains every nutrient needed in a balanced diet.',
'Chewing bread increases its surface area, helping enzymes contact the starch. Mechanical breakdown and chemical enzyme action work together, but are not the same process.',
'Compare a small intestine with many villi and one with damaged villi. Less effective surface area can reduce nutrient absorption even if digestion has broken food down normally.'],
{'digestion':'Breakdown of large food molecules into smaller absorbable molecules.','enzyme':'A biological catalyst that speeds a chemical reaction.','villus':'A small projection increasing the absorptive surface of the small intestine.'},[
('What is digestion?','Breakdown of large food molecules into smaller absorbable molecules.','Include the purpose of absorption.'),
('Which nutrient supplies amino acids for growth and repair?','Protein','Proteins are digested to amino acids.',['Protein','Fibre','Water']),
('Name the movement that carries food along the oesophagus.','Peristalsis','Coordinated muscle contractions move the food.'),
('Where does salivary amylase begin acting?','In the mouth.','It begins starch digestion.'),
('Where is bile produced?','The liver.','It is stored in the gall bladder.'),
('Is bile an enzyme?','No. It emulsifies fats and helps neutralise acid.','Lipase performs chemical digestion of fats.'),
('Where does most nutrient absorption occur?','The small intestine.','Its folds and villi increase surface area.'),
('Give two features of villi that aid absorption.','Large collective surface area, thin surfaces and a good blood supply; any two.','Explain how the features help movement or removal of nutrients.'),
('Distinguish egestion and excretion.','Egestion removes undigested material; excretion removes metabolic wastes.','Do not treat faeces as all metabolic waste.'),
('State a function of dietary fibre.','It helps normal movement of material through the bowel.','Fibre is not digested like starch in humans.'),
('What colour indicates starch in an iodine test?','Blue-black.','Record an observation before drawing the conclusion.'),
('Why can cows obtain nutrients from cellulose more effectively than humans?','Microorganisms in the ruminant digestive system help break down cellulose.','The microbial contribution is essential.'),
('Name two things that affect a person’s energy needs.','Age and activity level; other relevant factors are acceptable.','A balanced diet must match individual needs.'),
('Explain the benefit of chewing to chemical digestion.','It increases surface area for enzymes to act on.','Link mechanical breakdown to enzyme contact.'),
('Why must food-test reagents never be tasted?','They can be harmful chemicals and are not safe foods.','Use supervised laboratory handling only.')],['Trace digestion and absorption through the human gut.','Distinguish nutrient roles and digestive processes.','Interpret food-test observations safely.'])
add('mathematics',1,'real-numbers','Real numbers, inequalities and approximation',[2,3,4,5,9,10,11,12],[
'A rational number can be written as a/b, where a and b are integers and b is nonzero. Integers, terminating decimals and recurring decimals are rational. An irrational number cannot be written in this form; its decimal expansion neither terminates nor repeats. √2 is irrational but √9 = 3 is rational. The real numbers include both rational and irrational numbers and can be represented on a number line.',
'On a number line, numbers increase towards the right. Thus −2 is greater than −5 even though 5 has a greater magnitude than 2. Absolute value is distance from zero, so |−5| = 5 and |5| = 5. For inequalities, adding the same quantity to both sides preserves the direction. Multiplying or dividing by a negative number reverses the inequality sign: if −2x < 8, dividing by −2 gives x > −4.',
'To turn a recurring decimal into a fraction, let x equal the decimal, multiply by a suitable power of ten, and subtract equations so the repeating tails cancel. For x = 0.333…, 10x = 3.333…, so 9x = 3 and x = 1/3. For x = 0.272727…, 100x − x = 27 and x = 27/99 = 3/11. The number of repeated digits determines the useful power of ten.',
'Decimal places count digits after the decimal point, whereas significant figures count from the first nonzero digit. To round, inspect the next digit: in the usual school convention, increase the last retained digit if the next is 5 or more. Leading zeros are not significant. For example 0.00486 to two significant figures is 0.0049. Rounding introduces an approximation, so use ≈ when appropriate and avoid rounding every intermediate calculation unnecessarily.'],[
'Compare −7 and −3: −3 lies farther right, so −7 < −3. Their absolute values are 7 and 3 respectively.',
'Round 28.746 to two decimal places: retain 28.74 and inspect the next digit 6, giving 28.75. To two significant figures it becomes 29 instead.',
'Solve −3x ≥ 12: divide by −3 and reverse the sign, obtaining x ≤ −4. Check x = −5: 15 ≥ 12 is true.'],
{'rational number':'A number expressible as a ratio of integers with nonzero denominator.','absolute value':'Distance of a real number from zero.','significant figures':'Digits counted from the first nonzero digit to express numerical precision.'},[
('Is 0.125 rational? Explain.','Yes; 0.125 = 125/1000 = 1/8.','Provide an integer ratio.'),
('Which is irrational?','√2','√9 is 3 and 1/4 is an integer ratio.',['√2','√9','1/4']),
('Write 0.666… as a fraction in simplest form.','2/3','10x − x = 6, so x = 6/9.'),
('Convert 0.121212… to a fraction.','4/33','99x = 12, so x = 12/99 = 4/33.'),
('Which is greater: −8 or −2?','−2','It is farther right on a number line.'),
('Find |−12|.','12','Absolute value is a nonnegative distance.'),
('Solve x + 4 < 10.','x < 6','Subtract 4 from both sides.'),
('Solve −2x < 6.','x > −3','Reverse the inequality when dividing by −2.'),
('Round 7.836 to two decimal places.','7.84','The third decimal digit is 6.'),
('Round 0.00674 to two significant figures.','0.0067','The first significant digit is 6; the third is 4.'),
('Round 4860 to two significant figures.','4900','The third significant digit is 6.'),
('Estimate 19.8 × 5.1 using one-significant-figure values.','20 × 5 = 100','An estimate is not the exact product.'),
('State the difference between 3 decimal places and 3 significant figures.','Decimal places start after the point; significant figures start at the first nonzero digit.','Explain the starting position for each.'),
('Find the two possible numbers x if |x| = 7.','x = 7 or x = −7.','Both points are 7 units from zero.'),
('Why should intermediate calculations not be rounded too early?','Repeated rounding can accumulate error and change the final answer.','Keep extra digits until the final stated precision.')],['Classify and compare real numbers.','Convert recurring decimals and solve simple inequalities.','Round and estimate with stated precision.'])
add('mathematics',2,'quadratics','Quadratic equations and indices',[6,7,8,9],[
'A quadratic equation has a highest variable power of two and can be written ax² + bx + c = 0, with a ≠ 0. Always put the equation in this form before identifying a, b and c. The sign belongs with the coefficient: in x² − 5x + 6 = 0, b is −5. A root or solution is a value that makes the original equation true.',
'Factorisation writes a quadratic expression as a product. To factor x² + bx + c, look for two numbers whose sum is b and product is c. Since −2 and −3 sum to −5 and multiply to 6, x² − 5x + 6 = (x − 2)(x − 3). If a product is zero, at least one factor must be zero; therefore the roots are 2 and 3. Do not use the zero-product rule on a product that equals a nonzero number.',
'Completing the square rewrites an expression using a perfect square. For x² + 6x + 5 = 0, move 5, add 9 to both sides and obtain (x + 3)² = 4. Taking both square roots gives x + 3 = ±2, so x = −1 or −5. More generally the quadratic formula is x = [−b ± √(b² − 4ac)]/(2a). The entire numerator is divided by 2a. A negative discriminant means no real roots.',
'For a nonzero base a, a^m × a^n = a^(m+n), a^m/a^n = a^(m−n), (a^m)^n = a^(mn), a^0 = 1 and a^(−n) = 1/a^n. These rules require the same base when combining exponents by addition or subtraction. Standard form writes a number as A × 10^n with 1 ≤ A < 10 and n an integer. Thus 540,000 = 5.4 × 10^5 and 0.00072 = 7.2 × 10^−4.'],[
'Solve x² − 7x + 12 = 0. The numbers −3 and −4 have sum −7 and product 12, so (x−3)(x−4)=0 and x=3 or 4. Substitution confirms both.',
'Solve x² + 4x − 1 = 0. Here a=1, b=4, c=−1. x=[−4 ± √(16+4)]/2 = −2 ± √5.',
'Simplify 2³ × 2⁴ / 2² = 2^(3+4−2) = 2⁵ = 32. Combine exponents only because the base is consistently 2.'],
{'quadratic':'An expression or equation whose highest variable power is two.','discriminant':'The quantity b² − 4ac in a quadratic equation.','standard form':'Writing a number as A × 10^n with 1 ≤ A < 10.'},[
('Identify a, b and c in 2x² − 3x + 1 = 0.','a = 2, b = −3, c = 1.','Keep the negative sign on b.'),
('Factorise x² + 5x + 6.','(x + 2)(x + 3)','2 + 3 = 5 and 2 × 3 = 6.'),
('Solve x² − 9 = 0.','x = 3 or x = −3.','(x−3)(x+3)=0.'),
('Solve x² − 5x + 6 = 0.','x = 2 or 3.','Factor as (x−2)(x−3).'),
('Factorise x² − 4x − 5.','(x − 5)(x + 1)','−5 + 1 = −4 and −5 × 1 = −5.'),
('Complete the square: x² + 8x.','(x + 4)² − 16','Expanding the square gives x²+8x+16.'),
('Solve (x + 2)² = 9.','x = 1 or −5.','x + 2 = 3 or −3.'),
('Find the discriminant of x² − 4x + 4 = 0.','0','(−4)² − 4×1×4 = 0.'),
('Simplify 3² × 3³.','3⁵ = 243','Add exponents for a common base.'),
('Simplify 5⁶/5⁴.','5² = 25','Subtract exponents for a common nonzero base.'),
('Evaluate 7⁰.','1','Any nonzero base raised to zero equals 1.'),
('Evaluate 2⁻³.','1/8','A negative exponent gives a reciprocal.'),
('Write 630,000 in standard form.','6.3 × 10⁵','The first factor lies from 1 up to but not including 10.'),
('Write 0.00045 in standard form.','4.5 × 10⁻⁴','A negative exponent represents a small positive number.'),
('Explain why x² = 16 has two real solutions.','Both 4² and (−4)² equal 16, so x = ±4.','Include the negative solution.')],['Solve quadratics by factorisation, completing the square and formula.','Apply index laws correctly.','Convert numbers to standard form.'])
add('kiswahili',1,'aina-za-maneno','Aina za maneno na mpangilio wa sentensi',[3,4,10],[
'Maneno hutimiza kazi tofauti katika sentensi. Nomino hutaja mtu, kitu, mahali, hali au wazo, kwa mfano Amina, kitabu na furaha. Kiwakilishi husimama badala ya nomino katika muktadha, kwa mfano yeye katika Amina amefika; yeye amebeba kitabu. Kivumishi hutoa maelezo kuhusu nomino au kiwakilishi, kama kidogo katika kitabu kidogo. Usihukumu aina ya neno bila kuangalia matumizi yake katika sentensi.',
'Kitenzi hueleza tendo au hali: anasoma, wamefika na ni katika matumizi ya kuwa kiunganishi cha kiarifu. Vielezi hueleza zaidi kuhusu tendo au sifa, kwa mfano polepole katika anatembea polepole na jana katika alifika jana. Kihusishi huonyesha uhusiano, kwa mfano chini ya meza. Kiunganishi huunganisha vipashio, kama na, lakini na kwa sababu. Kihisishi huonyesha hisia, kama Lo! au Hongera!, kutegemea muktadha.',
'Sentensi yenye maana inahitaji uhusiano unaoeleweka baina ya maneno yake. Mtoto mdogo anasoma kitabu ina nomino mtoto, kivumishi mdogo, kitenzi anasoma na nomino kitabu. Kubadilisha mpangilio kiholela kunaweza kuficha maana. Kiswahili kinaweza kutumia kiambishi cha nafsi katika kitenzi bila kurudia kiima kwa neno tofauti: Ninasoma tayari huonyesha msemaji mmoja.',
'Unapoandika hadithi, chagua maneno yanayolingana na tukio na hadhira. Unganisha sentensi katika aya zenye wazo kuu, epuka kurukaruka muda bila sababu na tumia alama za uandishi. Majina mahsusi huanza kwa herufi kubwa. Nukta huonyesha mwisho wa sentensi ya taarifa; alama ya kuuliza hutumika kwa swali. Soma rasimu tena ili kukagua maana, upatanisho na mpangilio kabla ya kuwasilisha.'],[
'Katika sentensi Mwanafunzi hodari ameandika vizuri, mwanafunzi ni nomino, hodari kivumishi, ameandika kitenzi na vizuri kielezi. Uchambuzi unaangalia kazi ya kila neno hapa.',
'Sentensi Asha alisoma na Juma aliandika hutumia na kuunganisha taarifa mbili. Asha alisoma lakini hakumaliza hutumia lakini kuonyesha tofauti na matarajio.',
'Rasimu: juma alifika jana je alileta kitabu. Uhariri: Juma alifika jana. Je, alileta kitabu? Tumeweka herufi kubwa na kutofautisha taarifa na swali.'],
{'nomino':'Neno linalotaja mtu, kitu, mahali, hali au wazo.','kielezi':'Neno au kipashio kinachoeleza zaidi kuhusu tendo au sifa katika muktadha.','kiunganishi':'Neno linalounganisha vipashio vya lugha.'},[
('Taja nomino katika Mtoto anacheza.','Mtoto','Neno linamtaja anayefanya tendo.'),
('Kitenzi katika Asha ameandika barua ni kipi?','Ameandika','Kinaeleza tendo na taarifa ya nafsi na wakati/hali.'),
('Taja kivumishi katika kitabu kipya.','Kipya','Kinaeleza sifa ya kitabu.'),
('Neno polepole katika anatembea polepole lina kazi gani?','Ni kielezi kinachoeleza namna ya kutembea.','Chunguza matumizi katika sentensi hiyo.'),
('Tumia kiwakilishi badala ya Juma katika Juma amefika.','Yeye amefika.','Yeye hurejelea Juma katika muktadha.'),
('Unganisha: Nilifika. Sikukuta mtu. Tumia lakini.','Nilifika lakini sikukuta mtu.','Kiunganishi kinaonyesha tofauti.'),
('Tunga sentensi yenye kiunganishi kwa sababu.','Nilibeba mwavuli kwa sababu mvua ilinyesha.','Sentensi ionyeshe uhusiano wa sababu.'),
('Taja kihusishi katika Kitabu kiko juu ya meza.','Juu ya','Kinaonyesha uhusiano wa mahali.'),
('Taja mfano wa kihisishi.','Lo! au Hongera!','Kazi yake hutegemea hisia na muktadha.'),
('Sahihisha herufi kubwa: amina anaishi arusha.','Amina anaishi Arusha.','Majina mahsusi yanaanza kwa herufi kubwa.'),
('Weka alama sahihi: Je umefika','Je, umefika?','Hii ni sentensi ya swali.'),
('Eleza kwa nini Ninasoma inaweza kuwa sentensi yenye maana.','Kiambishi ni- kinaonyesha nafsi ya msemaji na kitenzi kinaeleza tendo.','Si lazima kiima kirudiwe kwa neno tofauti.'),
('Tunga sentensi yenye nomino na kivumishi.','Mwanafunzi mwerevu anasoma.','Nomino na kivumishi viwe na uhusiano sahihi.'),
('Tunga sentensi yenye kitenzi na kielezi.','Juma ameandika vizuri.','Kielezi kieleze tendo katika muktadha.'),
('Andika sentensi tatu zinazojenga aya kuhusu kusoma.','Kusoma kila siku huongeza maarifa. Mimi husoma kitabu baada ya kazi za shule. Tabia hii hunisaidia kuelewa masomo.','Pima wazo moja kuu, mpangilio na uhusiano wa sentensi.')],['Tambua kazi za aina za maneno.','Tunga sentensi na aya zenye uhusiano sahihi.','Hariri herufi kubwa na alama za uandishi.'])
add('kiswahili',2,'upatanisho','Ngeli na upatanisho wa kisarufi',[1,2,3],[
'Upatanisho wa kisarufi ni uhusiano wa kimaumbo kati ya nomino na vipashio vinavyoirejelea, kama vivumishi, viwakilishi na vitenzi. Katika kitabu kizuri kimepotea, ki- katika kizuri na kimepotea kinahusiana na kitabu. Katika vitabu vizuri vimepotea, umbo la wingi linaonekana katika vi-. Ngeli zinaweza kuchambuliwa kwa viambishi vya nomino au vya upatanisho; katika sura hii tunazingatia maumbo yanayotumika katika sentensi.',
'Nomino nyingi za watu na viumbe hai hupatana kwa a- katika umoja na wa- katika wingi wa vitenzi: mtoto anacheza; watoto wanacheza; paka amekula; paka wamekula. Hata hivyo, maumbo ya vivumishi na viwakilishi yanahitaji kuangaliwa katika matumizi husika. Usichukue kila neno linaloanza kwa ki- kuwa la ngeli moja bila kuchunguza maana na upatanisho wake: kipofu, akimaanisha mtu, anaweza kuhitaji upatanisho wa viumbe hai.',
'Mifano mingine ni mti mrefu umeanguka na miti mirefu imeanguka; jicho kubwa linauma na macho makubwa yanauma; nyumba nzuri imejengwa na nyumba nzuri zimejengwa. Nomino inaweza kubaki na umbo lilelile katika umoja na wingi lakini upatanisho ukabadilika, kama nyumba. Soma sentensi nzima ili kujua idadi na uhusiano, badala ya kutegemea umbo la nomino peke yake.',
'Sentensi ambatani huunganisha vishazi huru, kwa mfano Asha anasoma na Juma anaandika. Sentensi changamani ina kishazi kinachotegemea kingine, kwa mfano Mwanafunzi aliyefika mapema amepata nafasi. Katika uandishi, hakikisha virejeshi vinaendana na vinavyorejelewa: kitabu kilichopotea; vitabu vilivyopotea. Ukibadili nomino kuwa wingi, kagua kila kipashio kinachohusika katika sentensi, si kitenzi pekee.'],[
'Umoja: Kitabu hiki kipya kimefika. Wingi: Vitabu hivi vipya vimefika. Nomino, kionyeshi, kivumishi na kitenzi vimebadilika kwa kuzingatia wingi.',
'Umoja: Mti huu mrefu umeanguka. Wingi: Miti hii mirefu imeanguka. Usitumie vi- kwa sababu tu nomino iko katika wingi.',
'Makosa: Watoto mdogo amefika. Uhariri: Watoto wadogo wamefika. Tumeoanisha kivumishi na kitenzi na nomino ya wingi.'],
{'upatanisho':'Uhusiano wa kimaumbo wa vipashio vinavyorejelea nomino.','kishazi huru':'Kishazi kinachoweza kutoa taarifa kamili bila kutegemea kingine.','kishazi tegemezi':'Kishazi kinachohitaji kuhusishwa na kingine ili kukamilisha taarifa.'},[
('Weka wingi: Kitabu kizuri kimepotea.','Vitabu vizuri vimepotea.','Badili nomino, kivumishi na kitenzi.'),
('Kamilisha: Watoto ___fika.','Wamefika','wa- hupatana na watoto katika mfano huu.'),
('Weka wingi: Mti mrefu umeanguka.','Miti mirefu imeanguka.','Upatanisho wa miti ni mi-/i- katika vipashio hivi.'),
('Sahihisha: Vitabu hiki kimefika.','Vitabu hivi vimefika.','Kionyeshi na kitenzi vipatane na vitabu.'),
('Weka umoja: Macho makubwa yanauma.','Jicho kubwa linauma.','Nomino na viambishi vya upatanisho vinabadilika.'),
('Weka wingi: Nyumba nzuri imejengwa.','Nyumba nzuri zimejengwa.','Nomino hubaki, lakini kiambishi cha kitenzi hubadilika.'),
('Je, kuanza kwa ki- pekee kunatosha kutambua upatanisho wote?','Hapana; maana na matumizi ya sentensi pia yanahitaji kuchunguzwa.','Mfano wa kipofu akimaanisha mtu unaonyesha umuhimu wa maana.'),
('Kamilisha: Kitabu ___potea kimepatikana.','Kilichopotea','Kirejeshi kipatane na kitabu.'),
('Weka wingi: Kitabu kilichopotea kimepatikana.','Vitabu vilivyopotea vimepatikana.','Kagua kirejeshi na kitenzi pia.'),
('Tunga sentensi ambatani kwa kutumia lakini.','Juma alifika lakini Asha hakuwepo.','Unganisha vishazi viwili huru kwa uhusiano unaoeleweka.'),
('Tunga sentensi changamani yenye aliyefika.','Mwanafunzi aliyefika mapema amesaidia kupanga vitabu.','Kishazi aliyefika mapema kinategemea sehemu kuu.'),
('Sahihisha: Watoto mdogo amefika.','Watoto wadogo wamefika.','Vivumishi na vitenzi vipatane na nomino.'),
('Eleza maana ya upatanisho wa kisarufi.','Uhusiano wa kimaumbo kati ya nomino na vipashio vinavyoirejelea.','Toa mfano kuthibitisha ufafanuzi.'),
('Andika sentensi ya umoja na wingi kwa kutumia mwanafunzi.','Mwanafunzi huyu anasoma. Wanafunzi hawa wanasoma.','Kagua maumbo ya nomino, kionyeshi na kitenzi.'),
('Kwa nini sentensi nzima ichunguzwe wakati wa kuhariri wingi?','Nomino, vivumishi, viwakilishi, virejeshi na vitenzi vinaweza kuhitaji kubadilika pamoja.','Kubadili nomino pekee kunaweza kuacha makosa.')],['Tumia upatanisho katika umoja na wingi.','Hariri virejeshi, vivumishi na vitenzi.','Tofautisha sentensi ambatani na changamani.'])
add('geography',1,'earth-solar','Earth in the solar system',[2],[
'The solar system includes the Sun and the objects that move under its gravity, including planets, moons, asteroids and comets. Earth is the third planet from the Sun. In order outwards the eight planets are Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus and Neptune. The Sun is a star that emits light; planets are seen mainly by reflected sunlight. The Moon is Earth’s natural satellite, not a planet orbiting independently around the Sun in the same sense as Earth.',
'Earth is approximately spherical, with slight flattening near the poles and a bulge near the equator. Its mean radius is about 6371 km and its equatorial circumference about 40,075 km. These are approximate measurements, not values every school map needs at full precision. Evidence for its curved shape includes photographs from space, Earth’s curved shadow during lunar eclipses and changes in visible stars with latitude.',
'Earth rotates about its axis from west to east, completing a rotation relative to the Sun in about twenty-four hours. This produces the cycle of day and night: the part facing the Sun is illuminated while the other part is dark. Earth also revolves around the Sun in about 365¼ days. Its tilted axis and revolution cause changing day lengths and seasons; seasons are not mainly caused by changes in Earth’s distance from the Sun.',
'Latitude describes angular position north or south of the equator, from 0° to 90°. Longitude describes angular position east or west of the prime meridian, up to 180°. Parallels join points of equal latitude and meridians join the poles through points of equal longitude. Tanzania lies south of the equator, but exact coordinates depend on the location. A coordinate needs both its number and direction: 6°S is different from 6°N.',
'Earth turns roughly 360° in 24 hours, equivalent to 15° per hour or 1° in four minutes. This supports ideal local solar-time calculations, where a place farther east reaches solar noon earlier. Official civil time zones are chosen for practical and political reasons and do not always follow every 15° line. In a school calculation, first state whether the question asks for ideal local time or an official time-zone reading.'],[
'At a place with latitude 5°S, the angular position is five degrees south of the equator. Its longitude is still needed to locate it fully.',
'Two locations differ by 30° of longitude. Ideal local time differs by 30/15 = 2 hours. If B is east of A and A is at 10:00, B is at 12:00 local solar time.',
'Distinguish rotation and revolution: rotation is turning about Earth’s own axis and explains day/night; revolution is its orbit around the Sun and, together with axial tilt, helps explain seasons.'],
{'latitude':'Angular position north or south of the equator.','longitude':'Angular position east or west of the prime meridian.','rotation':'Turning about an object’s own axis.'},[
('Which planet is third from the Sun?','Earth','The sequence begins Mercury, Venus, Earth.'),
('Name the star at the centre of the solar system.','The Sun','It emits its own light.'),
('Is the Moon a planet or Earth’s natural satellite?','Earth’s natural satellite.','It orbits Earth while the Earth–Moon system moves around the Sun.'),
('What causes day and night?','Earth’s rotation.','Different parts face towards and away from the Sun.'),
('State Earth’s direction of rotation.','West to east.','This produces the Sun’s apparent east-to-west daily motion.'),
('Approximately how long is one revolution of Earth around the Sun?','365¼ days, about one year.','Distinguish a year from a day.'),
('What two factors chiefly produce the seasonal cycle?','Earth’s axial tilt and its revolution around the Sun.','Distance from the Sun is not the main explanation.'),
('What is the latitude of the equator?','0°','Latitude is measured north or south from it.'),
('What does 8°S indicate?','Eight degrees south of the equator.','It is a latitude, not a complete location.'),
('Name the line from which longitude is measured.','The prime meridian.','Longitudes are measured east or west of it.'),
('What are lines of equal latitude called?','Parallels','Meridians join equal-longitude positions.'),
('Calculate ideal local-time difference for 45° longitude separation.','3 hours','45 ÷ 15 = 3.'),
('B is 15° east of A. If A has local solar time 09:00, find B’s.','10:00','East is ahead in this ideal local-time calculation.'),
('Give two pieces of evidence for Earth’s curved shape.','Space photographs and the curved shadow during lunar eclipses; changes in visible stars are also valid.','Use evidence rather than simply naming a globe.'),
('Why may official clock time differ from an ideal longitude calculation?','Civil time-zone boundaries are chosen for practical and political reasons.','The 15° rule models local solar time, not every legal zone.')],['Locate Earth within the solar system.','Explain shape, rotation, revolution and seasons.','Use latitude, longitude and ideal local-time differences.'])
add('geography',2,'earth-systems','Earth’s layers and interacting systems',[1,2],[
'Earth has a thin outer crust, a much thicker mantle and a central core. Continental crust is generally thicker and less dense than oceanic crust. The mantle is mainly solid rock, but over long timescales some regions can flow slowly. Describing the whole mantle as a sea of liquid is misleading. The outer core is liquid and the inner core is solid, consisting mainly of iron with nickel and other constituents.',
'Temperature generally increases with depth, but pressure also increases and affects whether material is solid or liquid. The inner core remains solid despite its high temperature because of enormous pressure. The lithosphere consists of the crust and the rigid uppermost mantle, rather than the crust alone. Plates are sections of this rigid outer region. A classroom layered model simplifies a complex planet and is not a perfectly scaled representation.',
'The atmosphere is the envelope of gases around Earth. Most weather occurs in the lowest layer, the troposphere. The hydrosphere includes Earth’s water in oceans, rivers, lakes, ice, groundwater and water vapour. The biosphere includes life and the regions where organisms occur. These systems overlap and interact: water evaporates into air, rain enters soil and plants take up water through roots.',
'Water cycles through evaporation, condensation, precipitation, infiltration and runoff. Solar energy supports evaporation and gravity drives falling water and much surface flow. Removing vegetation can reduce interception and change runoff and erosion. Pollution released in one part of a catchment can affect water and living things elsewhere. A sound geographical explanation connects processes and evidence rather than presenting each system as isolated.'],[
'Compare crust and lithosphere: crust is a compositional layer; lithosphere includes the crust plus rigid upper mantle. Calling them identical loses the distinction.',
'Rain falls on a hillside. Some water infiltrates soil, some moves as runoff into a stream and some may later evaporate or be transpired by plants. The same event links water, land, air and living organisms.',
'A factory releases waste into a river. The immediate change is in the hydrosphere, but aquatic organisms in the biosphere may be affected and people downstream may lose a safe water source.'],
{'lithosphere':'The rigid outer Earth comprising crust and uppermost mantle.','hydrosphere':'All of Earth’s water in its different locations and states.','infiltration':'Entry of water from the ground surface into soil or rock.'},[
('Name Earth’s three broad internal layers.','Crust, mantle and core.','The core can be divided into outer and inner parts.'),
('Which part of the core is liquid?','The outer core.','The inner core is solid.'),
('Is the whole mantle liquid?','No; it is mainly solid rock, with some regions capable of slow flow.','Avoid the liquid-sea misconception.'),
('Which is usually thicker: continental or oceanic crust?','Continental crust.','Oceanic crust is generally thinner and denser.'),
('What does the lithosphere include?','The crust and rigid uppermost mantle.','It is not only the crust.'),
('Why can the inner core remain solid at high temperature?','Very high pressure affects its physical state.','Temperature alone does not determine whether material melts.'),
('Define atmosphere.','The envelope of gases surrounding Earth.','It includes several layers.'),
('In which atmospheric layer does most weather occur?','Troposphere','It is the lowest major atmospheric layer.'),
('Give three components of the hydrosphere.','Oceans, rivers and groundwater; ice, lakes and vapour are also valid.','Include water beyond oceans alone.'),
('What does biosphere refer to?','Living organisms and the regions where life occurs.','It interacts with water, air and land.'),
('Name the change from water vapour to liquid droplets.','Condensation','It is important in cloud formation.'),
('Distinguish infiltration and runoff.','Infiltration enters soil or rock; runoff flows over the surface.','State where water moves in each case.'),
('Explain one effect of removing vegetation from a steep slope.','More exposed soil can be eroded and runoff may increase.','Give a process link rather than an unsupported certainty.'),
('Explain a river-pollution link between two Earth systems.','Waste changes river water in the hydrosphere and can harm organisms in the biosphere.','Identify both systems and the connection.'),
('Why is a simple layered Earth model not a complete picture?','It simplifies scale, composition and variations within the layers.','Models aid explanation but have limits.')],['Compare crust, mantle, core and lithosphere.','Describe atmosphere, hydrosphere and biosphere.','Explain interactions through water-cycle and pollution examples.'])
add('business',1,'enterprise','Entrepreneurship and sole proprietorship',[1,2,3],[
'Business studies examines how people organise activities to produce, distribute and exchange goods and services. A good is a tangible item, such as a notebook; a service is an activity, such as bicycle repair or transport. Business decisions connect with mathematics through costing, languages through communication, geography through locations and transport, and science through products and production methods.',
'An entrepreneur identifies an opportunity, organises resources and accepts the uncertainty of starting or improving an enterprise. Useful skills include planning, keeping records, communicating, solving problems and adapting to evidence. Risk-taking does not mean gambling blindly: a careful entrepreneur estimates possible losses, tests demand and chooses affordable experiments. Profit can reward success, but it is not guaranteed.',
'An opportunity is more than an idea that sounds attractive. Investigate who needs the product, what alternatives they already use, whether they can pay and whether the business can deliver safely and lawfully at a sustainable cost. For example, many students may want low-cost stationery, but sales depend on school rules, competing sellers, purchasing times and reliable supply. Ask neutral questions rather than encouraging only the answer you hope to hear.',
'A sole proprietorship is owned by one person. The owner normally makes decisions and receives profits, but also carries responsibility for losses and business debts. Advantages can include simple decision-making and direct customer contact; disadvantages can include limited capital, heavy workload and lack of continuity if the owner cannot work. Ordinary sole proprietorship should not be confused with a limited-liability company. Before starting, an owner must check applicable registration, tax and sector requirements with the responsible authorities rather than assume a classroom example grants legal permission.'],[
'An entrepreneur notices that cyclists travel far for repairs. Before renting a workshop, she counts local bicycles, interviews potential customers and tests a small repair service. This reduces uncertainty without pretending it removes all risk.',
'A sole trader buys stock on credit and later cannot sell it. The debt is not automatically erased because the business name is different from the owner’s name; personal responsibility is a key disadvantage of ordinary sole proprietorship.',
'A notebook costs TSh 800 to buy and TSh 100 per unit in transport and handling. At a price of TSh 1000, the amount left before other costs is TSh 100. Ignoring the handling cost would overstate the margin.'],
{'entrepreneur':'A person who identifies opportunities and organises resources to establish or improve an enterprise.','sole proprietorship':'A business owned by one person who normally bears its obligations.','market research':'Gathering and analysing information about customers, demand and alternatives.'},[
('Distinguish a good and a service.','A good is tangible; a service is an activity supplied to meet a need.','Use an example of each.'),
('Give an example of a local service business.','Bicycle repair, tailoring or transport.','The main product is an activity.'),
('State two entrepreneurial skills.','Planning and communication; record keeping or problem solving are also valid.','Explain their use in an enterprise.'),
('Does entrepreneurship guarantee profit?','No. Demand, costs and other uncertainties can lead to losses.','Risk remains even with good planning.'),
('What makes a sole proprietorship different from a partnership?','It has one owner rather than multiple partners.','The distinction concerns ownership.'),
('Give one advantage of sole proprietorship.','The owner can make decisions quickly.','Direct customer contact or retaining profits may also be valid.'),
('Give one disadvantage of sole proprietorship.','The owner normally bears personal responsibility for business debts.','Limited capital and heavy workload are other valid disadvantages.'),
('Why should an entrepreneur investigate existing alternatives?','Customers may already have ways to meet the need, affecting demand and price.','Competition includes substitute services.'),
('Write one neutral market-research question for a stationery business.','Where do you currently buy exercise books, and what affects your choice?','Avoid leading questions that assume the business is desirable.'),
('Purchase cost is 600 and handling cost 100 per item. Find total unit cost.','TSh 700','Add both relevant costs.'),
('If that item sells for 900, find the amount remaining before other costs.','TSh 200','900 − 700 = 200; this is not necessarily final net profit.'),
('Explain one link between business and mathematics.','Mathematics supports calculating costs, revenue, profit and budgets.','Provide a concrete use.'),
('Why test a business idea at a small scale?','It supplies evidence about demand and costs while limiting possible losses.','A test reduces rather than eliminates uncertainty.'),
('Why is wanting a product different from effective demand?','A potential customer also needs willingness and ability to pay on the offered terms.','A wish alone does not ensure a sale.'),
('Outline three sensible steps before starting a sole-trader business.','Research customer needs, estimate resources and costs, and check relevant legal requirements.','Award credit for clear, practical preparation.')],['Explain goods, services and business links.','Evaluate entrepreneurial opportunities and skills.','Compare advantages and risks of sole proprietorship.'])
add('business',2,'production-capital','Production, capital and small-business resources',[1,2,3,5],[
'Production creates or increases the usefulness of goods and services. Growing maize, milling it, transporting flour and selling it all contribute to usefulness in different ways. Primary production obtains resources from nature, secondary production processes or manufactures products, and tertiary production supplies services. A service can be productive even when it creates no physical object.',
'The traditional factors of production are land, labour, capital and enterprise. Land includes natural resources; labour is human physical and mental effort; capital includes tools, equipment and other produced resources used to produce further output; enterprise coordinates resources and bears uncertainty. Money can finance productive capital, but money itself does not plough a field or repair a bicycle. A useful plan distinguishes finance from the assets and skills it will purchase.',
'A small business can obtain finance from personal savings, family contributions, loans or supplier credit. Loans require repayment under agreed terms and may involve interest, fees, collateral or group obligations. Supplier credit postpones payment but does not make goods free. Compare the full amount repayable, repayment dates and likely cash flow; do not judge an offer from the advertised instalment alone.',
'Cooperatives are member-owned organisations formed to meet shared needs, for example marketing crops or obtaining inputs. A savings and credit cooperative can help members save and obtain credit under its rules. Microfinance may provide small-scale financial services, but a small loan can still be costly or unsuitable. Membership obligations, charges, risks and governance should be understood before borrowing. This chapter explains concepts and is not a recommendation for any specific lender.',
'Warehousing involves safe storage until goods are needed. It can protect stock, support seasonal supply and allow larger purchases, but costs money and carries risks such as spoilage, theft and damage. Inventory records track stock received, issued and remaining. First-in, first-out handling can help move older dated stock before newer stock, but safe expiry rules still take priority. Reconcile recorded stock with physical counts to identify errors or loss.'],[
'Maize growing is primary production, milling flour is secondary production and transporting flour to customers is a tertiary service. Each activity adds usefulness to the chain.',
'A loan gives TSh 100,000 now and requires twelve payments of TSh 10,000 with no other charges. Total repayment is TSh 120,000 and finance cost is TSh 20,000. The example does not establish an annual percentage rate.',
'Opening stock is 40 bags, deliveries add 25 and sales remove 38. Expected closing stock = 40+25−38 = 27 bags. If only 24 are counted, investigate the difference of 3 rather than silently altering the record.'],
{'capital':'Produced resources used to create further goods or services.','supplier credit':'An arrangement allowing goods to be received before payment is due.','inventory':'Goods and materials held by a business, together with records of their quantities.'},[
('What is production?','Creating or increasing the usefulness of goods or services.','It includes services as well as manufacturing.'),
('Classify fishing as primary, secondary or tertiary production.','Primary','It obtains resources from nature.',['Primary','Secondary','Tertiary']),
('Classify flour milling.','Secondary production.','It processes an agricultural product.'),
('Classify transport of goods.','Tertiary production/service.','It adds place usefulness.'),
('Name the four traditional factors of production.','Land, labour, capital and enterprise.','Give all four and distinguish them.'),
('Give one example of productive capital in a tailoring business.','A sewing machine.','It is a produced resource used for further production.'),
('What is supplier credit?','Receiving goods with payment due at a later agreed time.','The payment obligation remains.'),
('Name two possible sources of small-business finance.','Personal savings and loans; family funds or supplier credit are also valid.','Identify sources rather than business expenses.'),
('A loan requires ten payments of 12,000. Find total repayment.','TSh 120,000','10 × 12,000 = 120,000.'),
('If the loan principal was 100,000 and there are no other charges, find finance cost.','TSh 20,000','120,000 − 100,000.'),
('Why check repayment dates as well as the total cost?','The business must have enough cash when each payment becomes due.','Profit over a whole year does not guarantee cash on a particular date.'),
('State one purpose of a cooperative.','Members work together to meet shared needs such as marketing produce or accessing inputs.','Emphasise member ownership and a shared purpose.'),
('Opening stock is 30, receipts 18 and issues 22. Find closing stock.','26 units','30 + 18 − 22 = 26.'),
('Give two risks of warehousing.','Theft and spoilage; damage or storage costs are also relevant.','Relate each to stored goods.'),
('Why compare stock records with a physical count?','To detect errors, unrecorded movements, damage or loss.','Investigate discrepancies instead of inventing transactions.')],['Explain production and its factors.','Compare capital sources and repayment obligations.','Calculate and check simple inventory records.'])
add('historia',1,'jamii-kabla-ukoloni','Jamii za Tanzania kabla ya ukoloni',[1,2,3,11,13,14,17,18],[
'Historia ya jamii za Tanzania kabla ya ukoloni inaonyesha mwingiliano, uhamaji na mabadiliko ya muda mrefu. Makundi yanayotajwa kwa lugha au asili si visiwa visivyohusiana. Watu walibadilishana maarifa, kuoana, kufanya biashara na kubadili shughuli za maisha kulingana na mazingira. Istilahi kama Wabantu na Wanilo zinaweza kusaidia kueleza uhusiano wa lugha na historia ya uhamaji, lakini hazimaanishi kila kundi lilikuwa na tabia, kazi au uwezo uleule.',
'Shughuli za kiuchumi zilihusisha kilimo, ufugaji, uvuvi, uwindaji, ukusanyaji, ufundi na biashara. Mazingira, teknolojia na mahitaji yaliathiri mchanganyiko wa shughuli hizo. Mfugaji angeweza kubadilishana mazao ya mifugo na nafaka kutoka kwa mkulima; jamii moja ingeweza kufanya kilimo na ufugaji kwa pamoja. Usihusishe shughuli moja na watu wote wa kundi fulani bila ushahidi wa mahali na kipindi.',
'Mifumo ya kisiasa ilitofautiana. Baadhi ya jamii zilikuwa na mamlaka iliyojikita kwa machifu au wafalme, huku nyingine zikitumia mabaraza ya wazee, ukoo au mifumo ya rika. Mamlaka ya kisiasa na mahusiano ya kijamii yaliathiri uamuzi kuhusu ardhi, migogoro, ulinzi na ushirikiano. Kutokuwa na ufalme mkuu hakumaanishi kutokuwa na utaratibu wa uongozi au sheria.',
'Utengenezaji wa vyombo, usindikaji wa chuma, ujenzi, tiba za jadi, uhifadhi wa chakula na maarifa ya mazingira ni mifano ya sayansi na teknolojia za jamii. Maarifa yalienezwa kupitia mafunzo ya vitendo, familia, mafundi na biashara. Mawasiliano na wageni yalileta bidhaa na mawazo mapya lakini pia yaliweza kuhusisha unyonyaji, vita na biashara ya watumwa. Tathmini mabadiliko kwa ushahidi na athari zake kwa makundi tofauti, badala ya kuyasifu au kuyakataa yote kwa kauli moja.'],[
'Jamii ya wakulima na wafugaji zinapobadilishana nafaka na maziwa, kila upande unapata bidhaa ambayo unaweza kukosa. Biashara hiyo huonyesha utegemeano, si kutengwa kabisa.',
'Mfua chuma anapofundisha mwanafunzi kuchagua na kutengeneza zana, maarifa ya kiufundi yanapitishwa kwa mazoezi. Bidhaa ya mwisho pekee haielezi hatua zote za teknolojia hiyo.',
'Baraza la wazee linaweza kusikiliza mgogoro wa matumizi ya ardhi. Huu ni mfano wa utaratibu wa kisiasa hata kama hakuna mfalme mwenye mamlaka juu ya eneo kubwa.'],
{'uhamaji':'Kuhama kwa watu kutoka eneo moja kwenda jingine kwa sababu mbalimbali.','mifumo ya rika':'Mpangilio wa kijamii unaohusisha makundi ya umri na majukumu yake.','ufundi':'Maarifa na stadi za kutengeneza au kurekebisha vitu kwa matumizi maalumu.'},[
('Taja shughuli tatu za kiuchumi kabla ya ukoloni.','Kilimo, ufugaji na uvuvi; ufundi na biashara pia zinakubalika.','Tofauti za maeneo na vipindi zizingatiwe.'),
('Je, kundi la lugha linaonyesha kwamba watu wake wote walifanya kazi moja?','Hapana. Shughuli zilitofautiana kwa mazingira, mahitaji na mabadiliko.','Epuka kauli za jumla zisizo na ushahidi.'),
('Toa mfano wa utegemeano kati ya wakulima na wafugaji.','Kubadilishana nafaka na bidhaa za mifugo.','Eleza namna pande zote zinavyonufaika.'),
('Taja mifano miwili ya utaratibu wa kisiasa wa kabla ya ukoloni.','Uongozi wa machifu na mabaraza ya wazee; mifumo ya ukoo au rika pia inakubalika.','Usidhani kulikuwa na mfumo mmoja tu.'),
('Je, kutokuwa na ufalme mkuu kulimaanisha kutokuwa na uongozi?','Hapana. Jamii zingetumia mabaraza, ukoo au mifumo mingine.','Tofautisha aina za mamlaka.'),
('Taja mfano wa teknolojia ya jamii za Tanzania kabla ya ukoloni.','Ufuaji wa chuma au uhifadhi wa chakula.','Eleza maarifa na matumizi yake.'),
('Maarifa ya ufundi yaliwezaje kurithishwa?','Kwa mafunzo ya vitendo kutoka kwa mafundi na familia.','Taja njia na uhusiano wake na stadi.'),
('Taja jambo moja lililoathiri shughuli za uchumi.','Mazingira, teknolojia au mahitaji ya jamii.','Eleza mfano badala ya kutaja jina pekee.'),
('Kwa nini historia ya uhamaji ihusishwe na ushahidi?','Ili kutofautisha madai, mabadiliko ya muda na tofauti za simulizi.','Tumia vyanzo zaidi ya kimoja inapowezekana.'),
('Toa mfano wa jukumu la uongozi kuhusu rasilimali.','Kusikiliza migogoro ya matumizi ya ardhi.','Lihusishe na uamuzi na mahusiano ya jamii.'),
('Je, biashara na wageni ilikuwa na athari nzuri tu?','Hapana; iliweza kuleta bidhaa na maarifa lakini pia unyonyaji na biashara ya watumwa.','Chunguza athari tofauti kwa ushahidi.'),
('Eleza sababu ya jamii kufanya kilimo na ufugaji pamoja.','Mchanganyiko unaweza kusaidia kupata vyakula na bidhaa tofauti na kukidhi mahitaji.','Usidai kwamba kila jamii ilifuata mfano huo.'),
('Taja maadili mawili yanayoweza kusaidia shughuli za pamoja.','Uaminifu na kuheshimu makubaliano.','Eleza jinsi yanavyosaidia ushirikiano.'),
('Pendekeza maswali mawili ya kuchunguza zana ya kale.','Ilitengenezwa kwa nyenzo gani na ilitumika kwa kazi gani?','Mahali, kipindi na muktadha pia ni maswali muhimu.'),
('Kwa nini jamii za kabla ya ukoloni zisielezwe kama zisizobadilika?','Ziliathiriwa na uhamaji, biashara, mazingira na mabadiliko ya teknolojia.','Onyesha mabadiliko ya muda mrefu.')],['Eleza tofauti na mwingiliano wa jamii kabla ya ukoloni.','Husisha uchumi na mifumo ya kisiasa na kijamii.','Tathmini teknolojia na maadili kwa ushahidi.'])
add('historia',2,'ukoloni-upinzani','Ukoloni, upinzani na harakati za uhuru',[1,2,4,5,6,7,8,9,10],[
'Ukoloni ni mfumo ambao dola ya nje hutawala jamii na eneo jingine kwa manufaa yake. Katika Afrika ya karne ya kumi na tisa, upanuzi wa himaya za Ulaya ulihusishwa na mashindano ya kisiasa, masoko, rasilimali na maslahi mengine. Mkutano wa Berlin wa 1884–1885 uliweka taratibu zilizosaidia mashindano ya kikoloni ya Ulaya; haukuwa mkutano ambao kila mpaka wa sasa wa Tanzania uliamuliwa mara moja wala ambao jamii za Afrika zilipewa nafasi sawa ya kuamua hatima yao.',
'Sehemu kubwa ya eneo la Tanganyika iliingia katika ukoloni wa Kijerumani mwishoni mwa karne ya kumi na tisa. Baada ya Vita Kuu ya Kwanza ya Dunia, Tanganyika iliwekwa chini ya utawala wa Uingereza katika mfumo wa mamlaka ya Shirikisho la Mataifa, baadaye udhamini wa Umoja wa Mataifa. Zanzibar ilikuwa na historia tofauti ya usultani na ulinzi wa Uingereza. Usichukulie Tanganyika na Zanzibar kuwa na historia ileile ya utawala katika kila kipindi.',
'Utawala wa kikoloni uliathiri ardhi, kazi, kodi, uzalishaji na elimu. Mahitaji ya kodi na kazi yanaweza kuonyesha namna uchumi ulivyoelekezwa kukidhi maslahi ya utawala na wafanyabiashara wa kikoloni. Jamii ziliitikia kwa njia mbalimbali, ikiwemo upinzani wa silaha, kukataa masharti, kuhama, mazungumzo na ushirikiano wa kimkakati. Njia iliyochaguliwa ilihusiana na mazingira na uwezo wa jamii, hivyo kukosekana kwa vita vya wazi si ushahidi wa kukubali kila sharti.',
'Vita vya Maji Maji vya 1905–1907 vilikuwa upinzani mkubwa dhidi ya utawala wa Kijerumani katika maeneo kadhaa ya kusini na mashariki ya Tanganyika. Sera za kazi na kilimo, ikiwemo masharti ya uzalishaji wa pamba, zilichangia malalamiko. Ukandamizaji wa kijeshi na uharibifu wa maisha na chakula ulileta mateso makubwa. Kujifunza harakati hizi kunahitaji kuheshimu waathiriwa na kutofautisha madai ya wakati huo, ushahidi wa kihistoria na tafsiri za baadaye.',
'Harakati za baadaye za uhuru zilijumuisha vyama, wafanyakazi, wakulima, viongozi wa jamii na mijadala ya kisiasa. TANU ilianzishwa mwaka 1954 na Tanganyika ilipata uhuru tarehe 9 Desemba 1961. Zanzibar ilipata uhuru tarehe 10 Desemba 1963 na Mapinduzi yalitokea tarehe 12 Januari 1964. Tanganyika na Zanzibar ziliungana tarehe 26 Aprili 1964. Tarehe hizi ni matukio tofauti; usiziunganishe kana kwamba uhuru, Mapinduzi na Muungano vilikuwa tukio moja.'],[
'Linganisho la maeneo: Tanganyika ilikuwa chini ya utawala wa Kijerumani na baadaye Uingereza; historia ya Zanzibar ilihusisha usultani na ulinzi wa Uingereza. Ufafanuzi sahihi unataja eneo na kipindi.',
'Mfanyakazi anapokataa sharti la kazi na mwingine akihama ili kuliepuka, wote wanaweza kuwa wanapinga hali fulani, ingawa mbinu zao si sawa na vita vya silaha.',
'Mpangilio wa matukio: TANU 1954 → uhuru wa Tanganyika 1961 → uhuru wa Zanzibar 1963 → Mapinduzi Januari 1964 → Muungano Aprili 1964. Mfuatano husaidia kuzuia kuchanganya matukio.'],
{'ukoloni':'Utawala wa dola ya nje juu ya jamii na eneo jingine kwa maslahi yake.','upinzani':'Hatua za kupinga mamlaka, masharti au mfumo unaokataliwa.','Muungano':'Kuungana kwa Tanganyika na Zanzibar tarehe 26 Aprili 1964.'},[
('Eleza maana ya ukoloni.','Utawala wa dola ya nje juu ya eneo na jamii nyingine kwa maslahi yake.','Husisha mamlaka na maslahi.'),
('Mkutano wa Berlin ulifanyika miaka gani?','1884–1885.','Usiuchanganye na vita vya Maji Maji.'),
('Je, jamii za Afrika zilipewa nafasi sawa katika mkutano huo?','Hapana.','Mkutano ulihusisha taratibu za mashindano ya kikoloni ya Ulaya.'),
('Ni dola gani ilitawala sehemu kubwa ya Tanganyika kabla ya Vita Kuu ya Kwanza?','Ujerumani.','Baadaye Uingereza ilitawala katika mfumo tofauti wa kimataifa.'),
('Kwa nini historia ya Zanzibar isitafsiriwe kama nakala ya Tanganyika?','Maeneo hayo yalikuwa na mifumo na mfuatano tofauti wa utawala.','Toa tofauti ya usultani/ulinzi na utawala wa Tanganyika.'),
('Taja athari mbili za ukoloni katika uchumi.','Mabadiliko ya matumizi ya ardhi na masharti ya kodi au kazi.','Linganisha maslahi ya watawala na athari kwa jamii.'),
('Taja njia mbili za upinzani zisizo vita vya silaha.','Kukataa masharti, kuhama, mazungumzo au ushirikiano wa kisiasa.','Eleza lengo la kupinga sharti fulani.'),
('Vita vya Maji Maji vinahusishwa na miaka gani?','1905–1907.','Taja kipindi badala ya tarehe moja ya uhuru.'),
('Taja chanzo kimoja cha malalamiko yaliyohusiana na Maji Maji.','Masharti ya kazi na uzalishaji wa pamba.','Malalamiko yalikuwa na vipengele kadhaa.'),
('TANU ilianzishwa mwaka gani?','1954','Ni kabla ya uhuru wa Tanganyika.'),
('Tanganyika ilipata uhuru lini?','9 Desemba 1961.','Hii si tarehe ya Muungano.'),
('Zanzibar ilipata uhuru lini?','10 Desemba 1963.','Mapinduzi yalitokea baadaye.'),
('Mapinduzi ya Zanzibar yalitokea lini?','12 Januari 1964.','Yatofautishe na uhuru wa 1963.'),
('Muungano wa Tanganyika na Zanzibar ulifanyika lini?','26 Aprili 1964.','Hili ni tukio tofauti na uhuru na Mapinduzi.'),
('Kwa nini kutokuwepo kwa vita vya wazi si ushahidi wa kukubali ukoloni?','Jamii zingeweza kutumia kukataa masharti, kuhama, mazungumzo au mbinu nyingine.','Pima aina tofauti za hatua na muktadha wake.')],['Eleza mifumo na athari za ukoloni.','Linganisha mbinu za upinzani na harakati za uhuru.','Panga matukio muhimu bila kuyachanganya.'])
add('english',1,'grammar-context','Grammar for everyday communication',[15,16,28,29,30,31,32],[
'The simple present often describes routines, facts and states. With I, you, we and they, use the base form for most verbs: I read; they walk. With he, she or it, add the appropriate ending: she reads; he watches. Questions and negatives normally use do or does with a base verb: Does she read? She does not read. Do not write does she reads, because does already carries the agreement.',
'The present progressive describes an activity in progress around the relevant present time: am/is/are + the -ing form. I am reading now contrasts with I read every evening. Use a form of be that agrees with the subject: we are studying, not we is studying. Some verbs for states, such as know in I know the answer, are usually expressed in the simple present rather than the progressive.',
'The simple past describes a completed event at a past time. Regular verbs often end in -ed, but many common verbs are irregular: go–went, write–wrote, see–saw and buy–bought. Past questions and negatives normally use did with the base form: Did you go? I did not go. A sentence can change tense when the time changes, but changing randomly makes a story confusing.',
'Articles and pronouns help the reader identify people and things. Use a/an for one non-specific countable item: a book, an egg. The choice depends on the following sound: an hour but a university. Use the when the reference is identified or otherwise specific in context. Possession can be shown with have/has, possessive pronouns or an apostrophe: Asha has a bag; the bag is hers; Asha’s bag. Possessive its has no apostrophe; it’s means it is or it has.',
'Directions combine clear sequence with location words: Walk past the library, turn left at the gate, and stop beside the office. Prepositions such as near, behind, between and opposite express relationships. Give a useful starting point and landmarks; avoid directions that depend on private knowledge. In spoken communication, listen to the request and check whether the person needs a repeated or simpler explanation.'],[
'Routine: Neema walks to school every day. Question: Does Neema walk to school every day? The main verb returns to walk after does.',
'Now: They are playing football. Yesterday: They played football. The time expressions explain why the tense changes.',
'Possession: This is Juma’s book. It is his. The apostrophe marks possession in Juma’s, while his is a possessive pronoun.'],
{'routine':'An activity done regularly.','present progressive':'A verb construction using am/is/are and an -ing form.','possessive pronoun':'A word such as mine, yours, hers or theirs that stands for an owned item.'},[
('Complete: She ___ books every evening.','reads','A third-person singular routine uses reads.',['reads','read','reading']),
('Correct: Does he walks to school?','Does he walk to school?','Use the base verb after does.'),
('Make negative: They study on Sundays.','They do not study on Sundays.','Use do not with the base verb.'),
('Complete: We ___ learning now.','are','We takes are in the progressive construction.'),
('Put in present progressive: I write a letter now.','I am writing a letter now.','Use am + writing.'),
('Give the simple past of buy.','Bought','It is an irregular form.'),
('Correct: Yesterday she go to town.','Yesterday she went to town.','Yesterday identifies a past event.'),
('Make a past question from You saw Asha.','Did you see Asha?','Use the base form see after did.'),
('Choose a or an: ___ hour.','An hour.','The word begins with a vowel sound.'),
('Choose a or an: ___ university.','A university.','The initial sound is /j/, like the start of you.'),
('Rewrite using a possessive pronoun: This bag belongs to Asha.','This bag is hers.','Hers replaces the noun phrase.'),
('Correct the possession: Its cover is red. Is an apostrophe needed in Its?','No. Its is the possessive form.','It’s with an apostrophe means it is or it has.'),
('Write a sentence with between and two landmarks.','The clinic is between the school and the market.','Identify both reference points.'),
('Give two clear directions from a gate to a library.','Walk straight from the gate, then turn right at the office towards the library.','A stated starting point and ordered actions matter.'),
('Explain the meaning difference: I read every evening / I am reading now.','The first is a routine; the second is an activity in progress now.','Connect grammar to meaning.')],['Use simple present, present progressive and simple past in context.','Apply articles and possession correctly.','Give clear directions using landmarks.'])
add('english',2,'inference-summary','Inference, summaries and connected ideas',[6,7,11,12,13,14,15],[
'An inference is a conclusion supported by clues and reasoning. It goes beyond repeating a stated fact, but it must remain consistent with the text. If a character closes a window as dark clouds approach, we may infer that rain is expected. We cannot infer the exact time the rain will begin unless the text supplies evidence. Separate what is stated, what is reasonably inferred and what remains unknown.',
'Read this original passage: The village library opened earlier during examination week. Halima arrived before sunrise, but several seats were already occupied. She chose a desk near the window and placed her notes beside a borrowed dictionary. When her friend asked her to leave for the market, she smiled and pointed to the revision timetable on the wall. After an hour, they compared answers to a science exercise. The passage suggests that preparation matters to Halima, without claiming that she studies every hour of every day.',
'A summary selects the main ideas and expresses them concisely in your own words. It omits minor details, repetitions and personal opinions unless the task asks for evaluation. Paraphrasing restates a particular idea, often at a similar level of detail; summarising reduces a larger text to its essentials. Preserve the meaning and avoid inventing motives or events. Use an appropriate word limit and check the summary against the source.',
'Word meanings can be inferred from surrounding ideas, but context may not provide a precise dictionary definition. In the passage, occupied suggests the seats were already being used. Prefixes and suffixes can help build vocabulary: un- can express the opposite, as in kind–unkind, and -ly can form some adverbs, as in careful–carefully. Not every word beginning with un or ending with ly follows a simple rule, so verify unfamiliar words in a suitable reference.',
'Cohesive devices make relationships clear. Moreover adds a supporting point, however introduces contrast, because gives a reason and therefore signals a result. Choose a connector that fits the logic. A summary should not simply string together every sentence with and. When combining accounts from several speakers, identify agreement and differences and keep track of who supplied each claim.'],[
'Literal detail: Halima used a borrowed dictionary. Inference: she had access to reference material for studying. Unsupported claim: she owned the dictionary; the passage says it was borrowed.',
'Possible summary: During examination week, Halima used the library early, followed a revision plan and worked with a friend on science answers. This keeps the main learning activities without every location detail.',
'Combine two ideas: The library opened early. Many seats were already occupied. Contrast: The library opened early; however, many seats were already occupied. The connector highlights an unexpected contrast.'],
{'inference':'A conclusion drawn from evidence and reasoning rather than directly stated.','summary':'A concise account of the main ideas in a longer text.','cohesive device':'A word or expression showing a relationship between ideas.'},[
('When did the library open earlier?','During examination week.','This is directly stated in the passage.'),
('Was Halima’s dictionary borrowed or owned?','Borrowed','Do not replace a stated detail with an assumption.',['Borrowed','Owned']),
('What suggests that other learners also valued early study?','Several seats were occupied before sunrise.','Link the observed detail to the inference.'),
('What did Halima point to when asked to leave?','The revision timetable on the wall.','Use the exact relevant detail.'),
('Does the passage prove that Halima never visits the market?','No. It describes only this occasion.','Avoid extending one event into an absolute claim.'),
('What does occupied mean in the seat description?','Already being used.','The surrounding context supports this meaning.'),
('Give the opposite of kind using a prefix.','Unkind','The prefix un- changes the meaning here.'),
('Form an adverb from careful.','Carefully','The spelling includes -fully.'),
('Which connector normally introduces contrast?','However','Moreover adds a point; therefore gives a result.',['However','Moreover','Therefore']),
('Which connector is suitable: She followed her timetable ___ she wanted to revise?','Because','It introduces a reason.'),
('State one difference between a summary and a paraphrase.','A summary condenses main ideas from a larger text; a paraphrase restates a particular idea without necessarily shortening it.','Both should preserve meaning.'),
('Write a one-sentence summary of the passage.','Halima studied early in the library during examination week, followed a plan and compared science answers with a friend.','Include main actions without adding unsupported details.'),
('Give one reasonable inference about Halima’s priorities on that morning.','She prioritised revision over going to the market at that time.','Qualify the claim to the particular occasion.'),
('Why should a summary normally omit personal opinions?','They add the writer’s evaluation rather than report the source’s main ideas.','Include evaluation only when the task requires it.'),
('How should conflicting oral accounts be summarised?','Attribute each claim, identify agreement and differences, and avoid presenting an unresolved claim as fact.','Keep the source of each claim clear.')],['Distinguish stated facts, inferences and unsupported assumptions.','Write concise summaries and paraphrases.','Use vocabulary and cohesive devices accurately.'])

def apply():
 p=ROOT/'content/library.json';d=json.loads(p.read_text());scope=json.loads((ROOT/'acquisition/curriculum-review.json').read_text()) if (ROOT/'acquisition/curriculum-review.json').exists() else json.loads((ROOT/'content/curriculum-map.json').read_text())['activities'];source={x['id']:x for x in scope}
 # Correct original form placement without changing stable lesson/question IDs.
 moves={'chemistry-f2-01':1,'physics-f2-01':1,'mathematics-f2-01':1,'geography-f1-01':2,'english-f2-01':1}
 for l in d['lessons']:
  if l['id'] in moves:l['form']=moves[l['id']];l['curriculumStatus']='supplemental-pending-full-mapping'
 for q in d['questions']:
  if q['topicIds'][0] in moves:q['form']=moves[q['topicIds'][0]]
 additions={'lessons':[],'questions':[],'glossary':[]}
 for chapter in chapters:
  sid=chapter['subjectId'];form=chapter['form'];lid=f'{sid}-f{form}-{chapter["slug"]}';lang='sw' if sid in ['kiswahili','historia'] else 'en'
  refs=[source[f'{sid}-f{form}-activity-{n:02}'] for n in chapter['refs']]
  citations=[{'activityId':r['id'],'sourceId':r['sourceId'],'pdfPages':r['pdfPages'],'scope':'partial-support'} for r in refs]
  l=dict(id=lid,form=form,subjectId=sid,topicId=lid,title=chapter['title'],language=lang,objectives=chapter['objectives'],paragraphs=chapter['paragraphs'],examples=chapter['examples'],summary=chapter['paragraphs'][0].split('. ')[0]+'.',glossary=list(chapter['terms']),diagram=None,curriculumStatus='source-referenced-partial',curriculumRefs=citations,publicationStatus='published',completionStatus='expanded-chapter')
  additions['lessons'].append(l)
  for i,(term,definition) in enumerate(chapter['terms'].items()):additions['glossary'].append(dict(id=f'{lid}-term-{i+1}',term=term,definition=definition,lessonId=lid))
  for i,item in enumerate(chapter['questions']):
   prompt,answer,feedback,*options=item;opts=options[0] if options else []
   additions['questions'].append(dict(id=f'{lid}-q{i+1:02}',paperId=None,form=form,subjectId=sid,topicIds=[lid],subtopicIds=[lid],sourceType='original',sourceTitle='SomaSmart original practice',institution='SomaSmart',year=None,curriculumEdition='TIE 2023; activity mapping partial',curriculumRefs=citations,questionNumber=str(i+1),parentQuestionId=None,type='mcq' if opts else 'short',instructions='',content=prompt,options=opts,media=[],maximumMarks=1 if opts else 2,markIncrement=1,answerKey=answer,markingGuide=feedback+(' Award up to 2 marks for the correct model response with the requested explanation/working; 1 for a correct key idea with an incomplete explanation.' if lang=='en' else 'Tumia alama 2 kwa jibu sahihi linalokidhi maelekezo; alama 1 kwa wazo kuu sahihi lenye maelezo pungufu.'),solutionProvenance='SomaSmart independently authored',sourceReference='Original authored expansion batch 2',rightsStatus='original',verificationStatus='author-reviewed',publicationStatus='published'))
 for collection,items in additions.items():
  existing={r['id']:i for i,r in enumerate(d[collection])}
  for row in items:
   if row['id'] in existing:d[collection][existing[row['id']]]=row
   else:d[collection].append(row)
 for b in d['books']:b['lessonIds']=[l['id'] for l in d['lessons'] if l['subjectId']==b['subjectId'] and l['form']==b['form']]
 d['version']='0.2.0';d['curriculum']['note']='Official Form I–II activity cells extracted for all nine subjects. New chapters carry page-level partial-support references. Full activity and subtopic coverage remains unfinished.'
 (ROOT/'content/batches/002-expansion.json').write_text(json.dumps(additions,ensure_ascii=False,indent=2));p.write_text(json.dumps(d,ensure_ascii=False,indent=2))
 print('Imported',len(additions['lessons']),'chapters and',len(additions['questions']),'original questions. Total:',len(d['lessons']),'chapters,',len(d['questions']),'questions.')
if __name__=='__main__':apply()
