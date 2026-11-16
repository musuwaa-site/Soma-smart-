"""Original authored starter chapters; no claim of complete syllabus coverage."""
import json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
subjects=[('chemistry','Chemistry','⚗','en'),('physics','Physics','↗','en'),('biology','Biology','❧','en'),('mathematics','Mathematics','∑','en'),('kiswahili','Kiswahili','Aa','sw'),('geography','Geography','◎','en'),('business','Business Studies','▥','en'),('historia','Historia ya Tanzania na Maadili','◈','sw'),('english','English Language','Ab','en')]
# Each entry: title, explanation paragraphs, three worked examples, glossary, six answerable activities.
chapters={
'chemistry':[
('Separating mixtures',[
'A mixture contains two or more substances that are physically combined. Its components retain their properties. A solution is a homogeneous mixture: dissolved salt is distributed throughout water. A suspension, such as muddy water, has particles that can settle. A pure substance has a fixed composition; visual clarity alone does not prove purity.',
'Choose a separation method using a difference in physical properties. Filtration separates an insoluble solid from a liquid. The solid left on the paper is the residue; the liquid passing through is the filtrate. Dissolved salt passes through filter paper with water, so filtration cannot recover it.',
'Evaporation removes a solvent to leave a dissolved solid. Crystallisation allows crystals to form from a concentrated solution, often on cooling. Simple distillation boils a liquid and condenses its vapour to collect the solvent. Never heat a sealed apparatus, taste laboratory chemicals or point a heated tube at anyone. School practical work requires teacher supervision.'],[
'Muddy water: allow large particles to settle, then filter. Mud is the residue and the water is the filtrate. Filtration alone does not make water safe to drink.',
'Salt water: evaporation can recover salt, but loses the water. Distillation collects water as a distillate while non-volatile salt remains behind.',
'Sand and salt: add water to dissolve salt, filter off sand, then evaporate the filtrate to obtain salt. The order matters because dry filtration cannot separate two powders.'],{'residue':'The solid retained by a filter.','filtrate':'The liquid that passes through a filter.','solvent':'A substance that dissolves a solute.'},[
('Which method separates sand from water?',['Filtration','Evaporation','Melting'],'Filtration','Sand is insoluble and is retained by filter paper.'),
('Which material passes through filter paper in salt solution?',['Only salt','Water and dissolved salt','Only water'],'Water and dissolved salt','Dissolved ions are not retained by ordinary filter paper.'),
('What is the liquid collected during distillation called?',None,'Distillate','Vapour cools and condenses to form the distillate.'),
('Explain how to separate a mixture of sand and salt.',None,'Dissolve salt in water; filter out sand; evaporate or crystallise the filtrate.','Award one mark for each correct stage, in order.'),
('Does clear filtered river water necessarily become safe to drink?', ['Yes','No'],'No','Filtration may leave microorganisms and dissolved contaminants.'),
('State one laboratory heating precaution.',None,'Do not heat sealed apparatus; use eye protection and teacher supervision.','Any one valid heating precaution earns the mark.')]),
('Particles and changes of state',[
'Matter is modelled as particles. In a solid, particles vibrate near fixed positions. In a liquid, particles remain close but move past one another. Gas particles are widely separated and move randomly. The model explains shape and compressibility; particles themselves do not expand when a substance is heated.',
'Melting changes a solid into a liquid. Freezing reverses melting. Boiling occurs throughout a liquid at its boiling temperature for a given pressure; evaporation occurs at a surface over a range of temperatures. Condensation changes gas to liquid. In a physical change, the chemical identity remains the same.',
'Diffusion is the net spreading of particles from a region of higher concentration to lower concentration due to random motion. It usually becomes faster as temperature rises. A smell spreading through air illustrates diffusion, but airflow may also move it.'],[
'Ice melts to water: H₂O molecules remain H₂O; the arrangement and movement change. This is a physical change.',
'A syringe containing air can be compressed because there is much space between gas particles. A sealed liquid-filled syringe is much harder to compress.',
'Water droplets outside a cold bottle come from water vapour in the surrounding air condensing on the cold surface, rather than water passing through the bottle.'],{'diffusion':'Net spreading due to random particle motion.','condensation':'Change from gas to liquid.','physical change':'A change that preserves chemical identity.'},[
('Which state has widely separated particles?',['Solid','Liquid','Gas'],'Gas','Gas particles have large spaces between them.'),
('Name the change from gas to liquid.',None,'Condensation','Cooling vapour can produce liquid droplets.'),
('Which change occurs throughout a liquid?',['Boiling','Evaporation'],'Boiling','Evaporation is a surface process.'),
('Explain why air is easier to compress than water.',None,'Gas particles have much larger spaces between them.','Credit the link between spacing and compressibility.'),
('During melting, do particles themselves become larger?',['Yes','No'],'No','Their arrangement changes, rather than particle size.'),
('Explain droplets on the outside of a cold bottle.',None,'Water vapour in air cools and condenses on the bottle.','Identify atmospheric vapour and condensation.')])],
'physics':[
('Measurement and density',[
'A measurement compares a quantity with a unit. Length has SI unit metre (m), mass kilogram (kg), and time second (s). Read a scale with your eye perpendicular to it to reduce parallax error. Record the unit as well as the number; 12 alone is not a complete length measurement.',
'Density is mass divided by volume: ρ = m/V. A material of mass 200 g occupying 100 cm³ has density 2 g/cm³. Compare densities only in compatible units. Since 1 g = 0.001 kg and 1 cm³ = 0.000001 m³, 1 g/cm³ = 1000 kg/m³.',
'For a regular block, measure length, width and height and multiply them to obtain volume. For an insoluble irregular solid, measure the increase in water level when fully submerged in a measuring cylinder. Avoid trapped bubbles and ensure water does not overflow. Repeat readings when possible.'],[
'A block is 5 cm × 2 cm × 3 cm. Volume = 5 × 2 × 3 = 30 cm³. If its mass is 90 g, density = 90/30 = 3 g/cm³.',
'A cylinder reads 40 cm³ before immersion and 65 cm³ after. Object volume = 65 − 40 = 25 cm³. For mass 50 g, density = 2 g/cm³.',
'Convert 2.5 g/cm³ to SI density: 2.5 × 1000 = 2500 kg/m³. Convert both mass and volume units, rather than just one.'],{'density':'Mass per unit volume.','parallax':'Apparent shift caused by viewing a scale from an angle.','volume':'Space occupied by an object.'},[
('What is the SI unit of mass?',['kg','m','s'],'kg','Mass is measured in kilograms.'),
('Calculate density for 60 g and 20 cm³.',None,'3 g/cm³','ρ = 60/20 = 3 g/cm³; one mark for substitution and one for answer with unit.'),
('A water level rises from 25 to 38 cm³. Find object volume.',None,'13 cm³','38 − 25 = 13 cm³.'),
('Convert 1.2 g/cm³ to kg/m³.',None,'1200 kg/m³','Multiply by 1000.'),
('How should the eye be placed when reading a scale?',None,'Perpendicular to the scale at the reading.','This reduces parallax.'),
('Which relation is correct?',['ρ = m/V','ρ = mV','ρ = V/m'],'ρ = m/V','Density is mass per unit volume.')]),
('Speed and distance–time graphs',[
'Distance is the length of a path travelled. Average speed is total distance divided by total time: v = d/t. Speed is a scalar: it has magnitude but no direction. Velocity includes a direction, so a journey returning to its starting point can have positive average speed but zero average velocity.',
'A distance–time graph places time on the horizontal axis and accumulated distance on the vertical axis. Its gradient represents speed. A horizontal section means the object is at rest. A steeper rising section indicates a greater speed if the axes use the same scales.',
'Convert units before substituting. To change km/h to m/s, divide by 3.6. For multiple journey sections, add all distances and all times, including stops, then divide. Averaging two speeds directly is generally wrong when the times spent at them differ.'],[
'A student travels 600 m in 120 s. Average speed = 600/120 = 5 m/s.',
'A cyclist travels 2 km in 10 min and stops for 5 min. Overall speed = 2000/900 = 2.22 m/s, including the stop.',
'Convert 36 km/h: 36 × 1000/3600 = 10 m/s. In 8 s at this speed, distance = vt = 10 × 8 = 80 m.'],{'speed':'Distance travelled per unit time.','gradient':'Vertical change divided by horizontal change.','scalar':'A quantity with magnitude and no direction.'},[
('Find the speed for 100 m in 20 s.',None,'5 m/s','100 ÷ 20 = 5 m/s.'),
('A horizontal distance–time graph means:',['Rest','Acceleration','Constant nonzero speed'],'Rest','Distance does not change as time passes.'),
('Convert 72 km/h to m/s.',None,'20 m/s','72 ÷ 3.6 = 20 m/s.'),
('Find distance at 4 m/s for 15 s.',None,'60 m','d = vt = 4 × 15 = 60 m.'),
('Is speed a vector or scalar?',['Scalar','Vector'],'Scalar','Speed does not specify direction.'),
('Why include stops in average journey speed?',None,'Total journey time includes time at rest.','Use total distance divided by total elapsed time.')])],
'biology':[
('Cells and organisation',[
'A cell is the basic structural and functional unit of living organisms. The cell membrane regulates movement of substances into and out of the cell. Cytoplasm is the region where many chemical reactions occur. In typical plant and animal cells, the nucleus contains genetic material and helps control cell activities.',
'Plant cells usually have a cellulose cell wall outside the cell membrane and a large permanent vacuole containing cell sap. Photosynthetic plant cells contain chloroplasts with chlorophyll. Not every plant cell has chloroplasts: many root cells do not. Animal cells have no cellulose cell wall or chloroplasts.',
'Similar specialised cells form a tissue; tissues cooperate in an organ; organs cooperate in an organ system. A leaf is an organ containing several tissues. Use a microscope carefully: begin with low power, focus safely, and keep lenses clean. A diagram should have clear lines, a title and labels that do not cross.'],[
'A leaf palisade cell contains many chloroplasts. These absorb light for photosynthesis, connecting its structure to its function.',
'A root hair cell has an elongated extension that increases surface area for absorption. It usually lacks chloroplasts because it is underground.',
'Cardiac muscle cell → cardiac muscle tissue → heart → circulatory system → organism. Each level includes interacting components.'],{'cell':'Basic structural and functional unit of life.','tissue':'A group of cells working together for a function.','chloroplast':'An organelle where photosynthesis occurs.'},[
('Which structure regulates movement across the cell boundary?',['Cell membrane','Nucleus','Vacuole'],'Cell membrane','The membrane is selectively permeable.'),
('Name a structure in a typical plant cell absent from an animal cell.',None,'Cellulose cell wall.','A chloroplast is also acceptable for a photosynthetic plant cell.'),
('Put organ, tissue and cell in increasing order of organisation.',None,'Cell → tissue → organ.','Cells form tissues, which form organs.'),
('Do all plant cells have chloroplasts?',['No','Yes'],'No','Many root cells do not photosynthesise.'),
('Why does a root hair have a long extension?',None,'It increases surface area for absorption.','Link the extension to absorption.'),
('State one feature of a good biological drawing.',None,'Clear unbroken lines with accurate labels.','A suitable title or non-crossing label lines is also valid.')]),
('Food chains and ecosystems',[
'An ecosystem includes organisms and their physical surroundings interacting together. A habitat is the place where an organism lives. Producers, such as green plants, make organic food using light energy. Consumers obtain food by eating organisms or their products.',
'A food-chain arrow points from the food to the feeder, showing energy transfer. Grass → grasshopper → frog → snake begins with a producer. Decomposers break down dead material and release nutrients that can be used again. Energy flows through the system and is dissipated as heat; nutrients cycle.',
'A food web links many food chains. Removing one species can affect several others, but the exact effect depends on alternative foods, disease and habitat. Burning vegetation can destroy habitats and expose soil. Conservation includes protecting habitats and using resources sustainably.'],[
'In maize → mouse → owl, maize is a producer, mouse a primary consumer and owl a secondary consumer. Arrows show the direction of energy transfer.',
'If insect numbers fall, an insect-eating bird may have less food. A bird that also eats seeds may be less affected than a specialist insect feeder.',
'Fungi break down dead leaves. Nutrients return to soil and can be absorbed by plants; this does not mean that energy is recycled.'],{'producer':'An organism that makes organic food from inorganic substances.','habitat':'The place an organism lives.','decomposer':'An organism that breaks down dead organic matter.'},[
('In grass → goat → human, identify the producer.',None,'Grass','Grass captures light energy and makes food.'),
('What do food-chain arrows represent?',['Energy transfer','Walking direction','Size'],'Energy transfer','The arrow points from food to feeder.'),
('Name one decomposer.',None,'Fungus','Many fungi and bacteria act as decomposers.'),
('Are energy and nutrients both recycled in an ecosystem?',['No','Yes'],'No','Nutrients cycle, whereas energy flows and dissipates as heat.'),
('Explain a possible effect of removing grass from a grazing habitat.',None,'Grazers lose food and may decline; their predators may also be affected.','Credit a justified chain of effects.'),
('Give one practical habitat conservation measure.',None,'Protect vegetation and prevent uncontrolled burning.','Accept a specific measure linked to habitat protection.')])],
'mathematics':[
('Fractions and proportional reasoning',[
'A fraction a/b represents a divided by b, where b ≠ 0. Equivalent fractions represent the same quantity: multiplying numerator and denominator by the same nonzero number preserves the value. Simplify using a common factor. A denominator describes the size of equal parts; it is not added when combining like fractions.',
'To add or subtract fractions, first express them with a common denominator. To multiply, multiply numerators and denominators, cancelling common factors where helpful. To divide by a nonzero fraction, multiply by its reciprocal. Check whether the result is reasonable.',
'A ratio compares quantities in the same units. To divide a total in ratio a:b, calculate a+b equal shares, then allocate a and b shares. A proportion states equal ratios. Percent means per hundred, so 15% = 15/100 = 0.15.'],[
'2/3 + 1/4 = 8/12 + 3/12 = 11/12. The least common denominator is 12.',
'3/5 ÷ 9/10 = 3/5 × 10/9 = 30/45 = 2/3. Multiplication by the reciprocal reverses division.',
'Divide TSh 24,000 in ratio 2:3. Total shares = 5. One share = 4800. The amounts are TSh 9600 and TSh 14,400; their sum is 24,000.'],{'denominator':'The nonzero number below a fraction bar.','reciprocal':'For a nonzero number x, the number 1/x.','ratio':'A comparison of quantities by division.'},[
('Simplify 12/18.',None,'2/3','Divide numerator and denominator by 6.'),
('Calculate 1/2 + 1/3.',None,'5/6','3/6 + 2/6 = 5/6.'),
('Calculate 3/4 × 2/5.',None,'3/10','6/20 simplifies to 3/10.'),
('Find 20% of 150.',None,'30','20/100 × 150 = 30.'),
('Divide 50 in the ratio 2:3. Give the smaller share.',None,'20','50/5 × 2 = 20.'),
('Which is equivalent to 3/4?',['6/8','3/8','4/3'],'6/8','Multiply both terms by 2.')]),
('Linear equations',[
'An equation states that two expressions have equal values. A solution is a value that makes the equation true. To preserve equality, perform the same operation on both sides. Expressions such as 3x + 2 contain a variable; 3x means 3 multiplied by x.',
'Solve a linear equation by simplifying brackets and collecting like terms, then isolating the variable. The distributive rule a(b+c)=ab+ac applies to every term inside the brackets. When a negative multiplier is outside brackets, it affects each sign inside.',
'Translate words carefully. Three more than twice a number is 2x+3; twice the sum of a number and three is 2(x+3). After solving, substitute into the original equation. A plausible-looking value is not enough: both sides must be equal.'],[
'3x + 5 = 20. Subtract 5 from both sides: 3x = 15. Divide by 3: x = 5. Check: 3(5)+5 = 20.',
'2(x − 4) = 10. Divide by 2: x − 4 = 5. Add 4: x = 9. Alternatively expand first to get 2x − 8 = 10.',
'A rectangle has perimeter 30 cm and length 9 cm. 2(9+w)=30; 9+w=15; w=6 cm. Check: 2(9+6)=30 cm.'],{'equation':'A statement that two expressions are equal.','variable':'A symbol representing a number.','solution':'A value that makes an equation true.'},[
('Solve x + 7 = 12.',None,'x = 5','Subtract 7 from both sides.'),
('Solve 4x = 28.',None,'x = 7','Divide both sides by 4.'),
('Solve 2x − 3 = 9.',None,'x = 6','Add 3 then divide by 2.'),
('Expand 3(x + 2).',['3x + 6','3x + 2','x + 6'],'3x + 6','Multiply each term in the brackets by 3.'),
('Solve 5(x − 1) = 20.',None,'x = 5','Divide by 5 to obtain x−1=4, then add 1.'),
('Explain how to check a proposed solution.',None,'Substitute it into the original equation and compare both sides.','Both sides must have the same value.')])],
'kiswahili':[
('Mawasiliano na ufahamu',[
'Mawasiliano ni mchakato wa kupeana na kupokea ujumbe. Mtumaji huwasilisha ujumbe kwa mpokeaji kupitia njia fulani. Lugha, ishara na picha zinaweza kufikisha ujumbe. Muktadha husaidia kuelewa maana: maneno yanayofaa kwa rafiki yanaweza kuhitaji kubadilishwa unapozungumza na mwalimu.',
'Usikilizaji makini unahitaji kuzingatia msemaji, kutambua hoja kuu na kuuliza swali la ufafanuzi bila kukatiza ovyo. Kelele na ujumbe usio wazi ni vikwazo vya mawasiliano. Mrejesho humsaidia mtumaji kutambua kama ujumbe umeeleweka.',
'Soma kifungu hiki: Asha aliona vitabu vimetapakaa darasani. Aliwaomba wenzake wamsaidie kuvipanga. Baada ya kazi, kila kitabu kilikuwa kwenye sehemu yake na wanafunzi walikipata kwa urahisi. Hoja kuu ni manufaa ya ushirikiano na utunzaji wa vifaa. Jibu swali kwa kutumia ushahidi wa kifungu, si kubuni tukio jipya.'],[
'Ujumbe: Tafadhali fika maktabani saa nne. Mtumaji ni anayetoa ombi; mpokeaji ni anayeombwa; ujumbe unaeleza mahali na wakati.',
'Swali: Kwa nini Asha aliomba msaada? Jibu: Vitabu vilikuwa vimetapakaa na alitaka vipangwe. Jibu linategemea kifungu.',
'Mwanafunzi anasema: Samahani mwalimu, naomba ufafanue hoja ya pili. Huu ni mrejesho wenye heshima unaoonyesha hitaji la maelezo zaidi.'],{'mrejesho':'Jibu linaloonyesha namna ujumbe ulivyopokelewa.','muktadha':'Mazingira yanayosaidia kutafsiri ujumbe.','ufahamu':'Uwezo wa kuelewa maana ya yaliyosomwa au kusikilizwa.'},[
('Mtu anayepokea ujumbe huitwaje?',['Mpokeaji','Mtumaji','Njia'],'Mpokeaji','Mpokeaji ndiye anayelengwa na ujumbe.'),
('Taja kikwazo kimoja cha mawasiliano.',None,'Kelele','Ujumbe usio wazi pia ni kikwazo.'),
('Kwa nini wanafunzi walivipata vitabu kwa urahisi baada ya kazi?',None,'Vitabu vilipangwa kwenye sehemu zake.','Tumia ushahidi wa kifungu.'),
('Andika ombi la heshima la kuazima kitabu.',None,'Tafadhali, naomba uniazime kitabu hiki.','Pima heshima na uwazi wa ombi.'),
('Nini maana ya mrejesho?',None,'Jibu linaloonyesha namna ujumbe ulivyopokelewa.','Jibu lieleze mwitikio wa mpokeaji.'),
('Taja hoja kuu ya kifungu cha Asha.',None,'Ushirikiano na utunzaji wa vitabu hurahisisha upatikanaji wake.','Kubali maelezo yanayounganisha kupanga na manufaa yake.')]),
('Uandishi wa aya na barua',[
'Aya ni mkusanyiko wa sentensi zinazojenga wazo moja kuu. Sentensi ya mada huanzisha wazo; sentensi zinazofuata hutoa maelezo, sababu au mifano. Aya nzuri ina mshikamano, yaani mawazo yanafuatana kwa namna inayoeleweka.',
'Kabla ya kuandika, tambua kusudi na msomaji. Panga hoja, andika rasimu, kisha hariri. Viunganishi kama kwa sababu, hata hivyo na kwa hiyo huonyesha uhusiano wa mawazo. Usitumie kiunganishi bila kuelewa kama kinaonyesha sababu, tofauti au matokeo.',
'Barua ya kirafiki inaweza kuwa na anwani ya mwandishi, tarehe, salamu, ujumbe na hitimisho. Ujumbe ubaki wazi na wenye heshima. Barua rasmi huhitaji mtindo unaolingana na taasisi na kusudi lake; hakiki maelekezo ya kazi kabla ya kuchagua muundo.'],[
'Sentensi ya mada: Maktaba yetu ina manufaa mengi. Maelezo: Tunapata vitabu vya rejea na mahali tulivu pa kusoma. Sentensi hizi zinajenga wazo moja.',
'Rasimu: Tulichelewa. Mvua ilinyesha. Uhariri: Tulichelewa kwa sababu mvua kubwa ilinyesha. Kiunganishi kinaonyesha sababu.',
'Ombi kwa rafiki: Nakuomba uniletee kitabu changu Jumamosi. Linaeleza kitu kinachohitajika na wakati unaotarajiwa.'],{'aya':'Kundi la sentensi zinazojenga wazo kuu moja.','rasimu':'Maandishi ya awali yanayoweza kuhaririwa.','mshikamano':'Muunganiko wa mawazo unaofanya matini ieleweke.'},[
('Aya nzuri hujengwa kuzunguka nini?',['Wazo kuu moja','Mada nyingi zisizohusiana'],'Wazo kuu moja','Sentensi saidizi huendeleza wazo hilo.'),
('Tunga sentensi yenye kwa sababu.',None,'Nilisoma kwa sababu nilitaka kuelewa somo.','Pima matumizi sahihi ya uhusiano wa sababu.'),
('Nini maana ya rasimu?',None,'Maandishi ya awali kabla ya uhariri.','Rasimu inaweza kurekebishwa.'),
('Taja mambo mawili ya kuangalia unapohariri.',None,'Tahajia na mpangilio wa mawazo.','Sarufi, alama na uwazi pia zinakubalika.'),
('Andika aya fupi kuhusu usafi shuleni.',None,'Usafi shuleni hulinda afya. Tuweke taka katika vyombo maalumu na tusafishe madarasa. Kwa kufanya hivyo tunapata mazingira mazuri ya kujifunza.','Alama 1 kwa wazo kuu, 1 kwa maelezo na 1 kwa mshikamano.'),
('Kwa hiyo huonyesha uhusiano gani?',['Matokeo','Salamu','Anwani'],'Matokeo','Huunganisha sababu au hali na tokeo lake.')])],
'geography':[
('Maps, direction and scale',[
'A map represents an area using selected symbols and a scale. A title states what is shown, a key explains symbols and a direction indicator helps orient the reader. North, east, south and west are the cardinal directions. Check the north indicator instead of assuming every page has north at the top.',
'A representative fraction such as 1:50,000 means one unit on the map represents 50,000 of the same units on the ground. Thus 1 cm represents 50,000 cm = 500 m. A larger denominator corresponds to a smaller scale, showing less detail over a larger area.',
'For a straight-line distance, measure between locations with a ruler and apply the scale. A winding route may be measured with a thread or short segments, then converted. Map distance and ground distance must use the same units before forming a ratio.'],[
'On a 1:50,000 map, 4 cm represents 4 × 50,000 = 200,000 cm = 2 km.',
'A school lies east of a clinic. From the school, the clinic is west. Reverse direction when changing the starting point.',
'A 1:25,000 map shows more detail than a 1:100,000 map for the same paper area. One centimetre represents 250 m rather than 1000 m.'],{'scale':'Relationship between map distance and ground distance.','key':'Explanation of symbols on a map.','cardinal directions':'North, east, south and west.'},[
('At 1:50,000, what does 2 cm represent?',None,'1 km','2 × 50,000 cm = 100,000 cm = 1 km.'),
('What explains map symbols?',['Key','Border','Date'],'Key','The key identifies the meaning of each symbol.'),
('What direction is opposite north?',None,'South','North and south are opposite directions.'),
('Which shows more detail?',['1:25,000','1:100,000'],'1:25,000','Its ground coverage per centimetre is smaller.'),
('Convert 500 m to centimetres.',None,'50,000 cm','500 × 100 = 50,000.'),
('Why is a straight ruler measurement insufficient for a winding road?',None,'It measures the direct separation rather than the full curved route.','Measure along the route using segments or thread.')]),
('Weather observations',[
'Weather is the condition of the atmosphere at a particular place and time. Climate describes long-term weather patterns. Temperature, rainfall, humidity, pressure, wind and cloud cover are weather elements. A single rainy day does not establish a climate trend.',
'A rain gauge measures precipitation depth in millimetres. Place it upright at a suitable open site away from obstructions and splashing. A thermometer measures temperature; suitable shelter protects an air-temperature sensor from direct solar radiation while allowing airflow.',
'Record observations with date, time, location and units. Daily temperature range is maximum minus minimum temperature. A mean requires adding readings and dividing by their count. Missing observations should be marked missing, not invented as zero.'],[
'Maximum temperature 31°C and minimum 19°C give a daily range of 31 − 19 = 12°C.',
'Rainfall readings 8, 0 and 10 mm total 18 mm over three days. A zero records an observed dry day; a missing reading is not the same thing.',
'Temperatures 20, 24 and 28°C have mean (20+24+28)/3 = 24°C. Equal weighting assumes the specified readings are being averaged.'],{'weather':'Atmospheric conditions at a place and time.','climate':'Long-term patterns of weather.','range':'Maximum value minus minimum value.'},[
('What instrument measures rainfall?',['Rain gauge','Thermometer','Wind vane'],'Rain gauge','It records precipitation depth.'),
('Find temperature range from 18°C to 30°C.',None,'12°C','30 − 18 = 12°C.'),
('Is one hot day enough to establish climate change?',['No','Yes'],'No','Climate concerns long-term patterns.'),
('Find the mean of 22, 24 and 26°C.',None,'24°C','72 ÷ 3 = 24°C.'),
('Why keep a rain gauge away from a roof?',None,'Runoff or shelter from the roof can distort rainfall measurements.','Link siting to accurate measurement.'),
('How should an unobserved rainfall day be recorded?',None,'As missing, rather than zero.','Zero means a measurement confirmed no rainfall.')])],
'business':[
('Needs, wants and scarce resources',[
'A need is something essential for well-being, such as adequate food, safe water and shelter. A want is something a person would like beyond basic needs. The classification depends on context: a phone may support essential work, while an expensive upgrade may mainly satisfy a preference.',
'Resources such as time, labour, land and capital are limited. Scarcity means choices must be made because available resources cannot satisfy every competing use. Opportunity cost is the value of the next best alternative forgone, not the sum of every possible alternative.',
'A budget lists expected income and planned spending over a stated period. Separate necessary spending from optional spending and allow for saving or emergencies where possible. A balanced budget has planned spending no greater than available funds. Money saved remains a use of income, rather than extra income.'],[
'A student has TSh 5000 and chooses a dictionary instead of a football. If the football was the next best option, it is the opportunity cost of the choice.',
'Weekly income is TSh 20,000. Food 9000 + transport 6000 + saving 3000 = 18,000. Unallocated balance = 2000.',
'A household compares repair and replacement. A cheaper purchase is not always cheaper overall if running and maintenance costs are higher. Compare costs over the relevant time.'],{'scarcity':'Limited resources relative to competing wants.','opportunity cost':'The next best alternative forgone when a choice is made.','budget':'A plan for income and expenditure over a period.'},[
('Which is a basic need?',['Safe drinking water','Luxury watch','Game console'],'Safe drinking water','Adequate safe water is essential to health.'),
('Define opportunity cost.',None,'The next best alternative forgone.','It is not all alternatives added together.'),
('Income is 12,000 and spending 9500. Find the balance.',None,'TSh 2500','12,000 − 9500 = 2500.'),
('Is saving the same as borrowing?',['No','Yes'],'No','Saving sets aside existing funds; borrowing creates a repayment obligation.'),
('Give one reason to prepare a budget.',None,'To plan spending within available income.','Accept prioritising needs or planning savings.'),
('Explain why time is a scarce resource.',None,'Time is limited and competing activities cannot all use the same hours.','Link a limit to the need to choose.')]),
('Revenue, costs and simple records',[
'A business keeps records to understand what it receives, spends, owns and owes. Revenue is money earned from sales before deducting costs. Profit is revenue minus the relevant total costs over the same period. A cash receipt is evidence of payment; it is not itself a profit calculation.',
'For identical items sold at one price, sales revenue = selling price × quantity sold. Cost of goods sold relates to the items sold; unsold stock should not automatically be treated as if it generated sales. For an introductory example with no opening or closing stock, profit can be calculated by subtracting purchase and operating costs from sales.',
'A simple cash record has date, description, money in, money out and running balance. Credit sales and purchases involve payment later, so profit and cash on hand can differ. Keep supporting documents and reconcile the record with actual cash.'],[
'A trader sells 20 notebooks at TSh 1500 each. Revenue = 20 × 1500 = TSh 30,000.',
'All notebooks cost TSh 18,000 and transport costs TSh 2000. If all are sold for TSh 30,000, profit = 30,000 − 18,000 − 2000 = TSh 10,000.',
'Opening cash 5000; cash received 8000; cash paid 6500. Closing cash = 5000+8000−6500 = TSh 6500.'],{'revenue':'Income earned from sales before deducting costs.','profit':'Revenue less relevant costs.','credit sale':'A sale for which payment is due later.'},[
('Sell 10 items at TSh 2000. Find revenue.',None,'TSh 20,000','10 × 2000 = 20,000.'),
('Revenue is 50,000 and costs 38,000. Find profit.',None,'TSh 12,000','50,000 − 38,000 = 12,000.'),
('Which document acknowledges a payment?',['Receipt','Weather chart','Map'],'Receipt','A receipt is evidence of payment.'),
('Find closing cash: opening 4000, receipts 6000, payments 3000.',None,'TSh 7000','4000 + 6000 − 3000 = 7000.'),
('Does a credit sale always increase cash immediately?',['No','Yes'],'No','Payment is due later.'),
('State why a business should keep supporting documents.',None,'They provide evidence for checking transactions and records.','Credit auditability or resolving disputes.')])],
'historia':[
('Vyanzo vya historia na ushahidi',[
'Historia huchunguza maisha na matukio ya binadamu katika nyakati zilizopita kwa kutumia ushahidi. Vyanzo vinaweza kuwa simulizi, maandishi, picha, vitu vya kale na mabaki ya majengo. Kila chanzo kina uwezo na mipaka; kutaja chanzo pekee hakuthibitishi kila dai linalotolewa.',
'Chanzo cha msingi kinatokana moja kwa moja na kipindi au tukio linalochunguzwa, kama barua ya mshiriki. Chanzo cha pili huchanganua au kueleza vyanzo vingine. Uainishaji hutegemea swali la utafiti: kitabu cha zamani kinaweza kuwa ushahidi wa mawazo ya kipindi kilipoandikwa.',
'Mtafiti huuliza: Nani alitengeneza chanzo? Lini? Kwa kusudi gani? Analinganisha ushahidi kutoka vyanzo tofauti badala ya kutegemea kumbukumbu moja. Simulizi zinahifadhi maarifa muhimu lakini kumbukumbu na mitazamo zinaweza kutofautiana. Heshimu mtoa taarifa na pata ridhaa kabla ya kurekodi mahojiano.'],[
'Barua iliyoandikwa wakati wa tukio inaweza kuwa chanzo cha msingi kuhusu mawazo ya mwandishi. Hata hivyo, huenda mwandishi hakushuhudia kila jambo alilotaja.',
'Wazee wawili wakitoa tarehe tofauti ya tukio, linganisha simulizi zao na kumbukumbu nyingine. Usichague tarehe kwa sababu msemaji mmoja anaongea kwa kujiamini zaidi.',
'Chungu cha kale kinaweza kutoa ushahidi kuhusu teknolojia au matumizi ya vyombo. Mahali kilipopatikana na mazingira yake ni muhimu; kukiondoa bila kumbukumbu hupoteza taarifa.'],{'ushahidi':'Taarifa au kitu kinachotumika kuchunguza dai.','chanzo cha msingi':'Chanzo kinachohusiana moja kwa moja na kipindi au tukio linalochunguzwa.','simulizi':'Maelezo yanayowasilishwa kwa mdomo.'},[
('Taja chanzo kimoja cha historia.',None,'Simulizi','Maandishi, picha na vitu vya kale pia vinakubalika.'),
('Je, chanzo kimoja kinathibitisha kila dai bila kuchunguzwa?',['Hapana','Ndiyo'],'Hapana','Chanzo kinaweza kuwa na mipaka au upendeleo.'),
('Kwa nini tunalinganisha vyanzo?',None,'Ili kutathmini usahihi na kutambua tofauti au mapungufu ya taarifa.','Jibu liunganishe ulinganishi na uchunguzi wa dai.'),
('Taja swali la kumuuliza mtunzi wa chanzo.',None,'Ulitengeneza chanzo hiki lini na kwa kusudi gani?','Nani, lini na kusudi ni maswali muhimu.'),
('Nini kifanyike kabla ya kurekodi mahojiano?',None,'Kupata ridhaa ya mtoa taarifa.','Heshimu faragha na masharti ya mtoa taarifa.'),
('Kwa nini mahali kilipopatikana kitu cha kale ni muhimu?',None,'Mazingira yake husaidia kutafsiri matumizi na uhusiano wake na vitu vingine.','Hifadhi muktadha wa ushahidi.')]),
('Maadili, uwajibikaji na utunzaji wa urithi',[
'Maadili ni kanuni na mitazamo inayosaidia kutathmini mwenendo wa watu. Uaminifu unahusisha kusema ukweli na kutotumia vibaya mali au taarifa. Uwajibikaji unahusisha kutimiza wajibu na kueleza maamuzi na matokeo yake.',
'Urithi wa kihistoria unaweza kuwa majengo, maeneo, nyaraka, sanaa, lugha na maarifa yanayorithishwa. Kuuhifadhi kunahitaji kuheshimu jamii zinazouhusisha na historia yao. Usiharibu wala kuondoa vitu kwenye eneo la kihistoria; fuata sheria na maelekezo ya mamlaka husika.',
'Katika mjadala, tofautisha ukweli unaoungwa mkono na ushahidi na maoni. Sikiliza hoja tofauti kwa heshima. Kutatua mgogoro kwa amani kunahitaji kubaini tatizo, kusikiliza pande zote na kutafuta suluhu inayoheshimu haki badala ya vitisho.'],[
'Mwanafunzi akipata kitabu cha mwenzake, anakirudisha badala ya kukificha. Huu ni mfano wa uaminifu na kuheshimu mali.',
'Kikundi kinapanga kusafisha mazingira ya eneo la urithi kwa ushauri wa wahusika. Hakigusi vitu vya kale bila ruhusa au utaalamu.',
'Wanafunzi wanapogombania kifaa cha kujifunzia, wanaweza kukubaliana ratiba ya matumizi baada ya kila mmoja kueleza hitaji lake.'],{'uwajibikaji':'Kutimiza wajibu na kuwa tayari kueleza maamuzi na matokeo.','urithi':'Mali na maarifa yenye thamani yanayorithishwa kutoka vizazi vilivyotangulia.','uaminifu':'Kusema ukweli na kutotumia vibaya mali au dhamana.'},[
('Kurudisha mali iliyopotea ni mfano wa nini?',['Uaminifu','Udanganyifu','Uharibifu'],'Uaminifu','Kunaheshimu mwenye mali na ukweli.'),
('Taja mfano wa urithi usio jengo.',None,'Lugha au maarifa ya jadi.','Sanaa na nyaraka pia ni mifano.'),
('Je, ni sahihi kuandika jina kwenye ukuta wa eneo la kihistoria?',['Hapana','Ndiyo'],'Hapana','Kitendo hicho kinaweza kuharibu urithi.'),
('Pendekeza hatua ya kwanza ya kutatua mgogoro kwa amani.',None,'Sikiliza pande zote na bainisha tatizo bila vitisho.','Pima heshima na ufafanuzi wa tatizo.'),
('Eleza maana ya uwajibikaji kwa mfano wa shule.',None,'Kiongozi wa kikundi anatimiza kazi na kueleza namna vifaa vilivyotumika.','Unganisha wajibu na kueleza matokeo.'),
('Kwa nini jamii ihusishwe katika utunzaji wa urithi?',None,'Ina uhusiano na maarifa kuhusu urithi na inaathiriwa na maamuzi ya utunzaji.','Kubali hoja inayoheshimu nafasi ya jamii.')])],
'english':[
('Reading for meaning',[
'Good readers identify the purpose, main idea and supporting details of a text. Skimming gives an overview; scanning locates a particular detail such as a date or name. Close reading examines the words and their relationships carefully. Choose the strategy that matches the task.',
'Read this original passage: Neema planted three seedlings near her home. During the dry week, she watered them each evening using water left from rinsing vegetables. Her brother made a small fence to protect them from goats. Two months later, all three seedlings had new leaves. The passage describes practical care for young plants.',
'A literal question asks for information stated directly. An inference combines clues with reasoning, but should not contradict the text. The passage suggests teamwork, because Neema watered the plants and her brother protected them. It does not state the species of tree or the exact volume of water used.'],[
'Question: How many seedlings did Neema plant? Answer: Three. This detail is explicitly stated in the first sentence.',
'Question: Why was a fence useful? Answer: It protected the seedlings from goats. The passage supplies this reason directly.',
'Question: What suggests cooperation? Answer: Neema watered the seedlings while her brother built a fence. Both contributed different kinds of care.'],{'skimming':'Reading quickly for the general meaning.','scanning':'Looking through text for a specific detail.','inference':'A reasoned conclusion supported by clues.'},[
('How many seedlings did Neema plant?',['Three','Two','Five'],'Three','The opening sentence states three seedlings.'),
('Who made the fence?',None,'Her brother','The passage identifies her brother.'),
('Why did the seedlings need protection?',None,'To protect them from goats.','The fence reduced access by goats.'),
('Which strategy is best for finding a specific name?',['Scanning','Skimming'],'Scanning','Scanning searches for a particular detail.'),
('Does the passage state the species of seedlings?',['No','Yes'],'No','Do not invent details absent from the text.'),
('Explain one sign of cooperation in the passage.',None,'Neema watered the plants and her brother made a protective fence.','Identify both contributions and their shared purpose.')]),
('Paragraphs and tense consistency',[
'A paragraph develops one main idea. A topic sentence introduces it, supporting sentences explain it with details or examples, and a closing sentence can complete the thought. Use connectors to show relationships, rather than listing unrelated sentences.',
'The simple past describes completed events at a past time: visited, walked, wrote. Some verbs are irregular: go becomes went, not goed. The present perfect uses has or have with a past participle and can connect a past event to the present: She has written a letter. Avoid changing tense without a reason.',
'When revising, check subject–verb agreement, tense, punctuation and clarity. He walks uses a singular present-tense verb; they walk uses the plural form. A complete sentence normally contains a subject and a finite verb. Read a draft aloud to hear missing words or awkward connections.'],[
'Draft: Yesterday we go to the library. Correction: Yesterday we went to the library. The time marker yesterday calls for the past tense.',
'Topic: Our school garden supports learning. Detail: We observe plant growth and practise measuring beds. The detail develops the topic rather than changing it.',
'Combine: It rained. We stayed indoors. Result: It rained, so we stayed indoors. The connector so expresses the result.'],{'topic sentence':'A sentence introducing the main idea of a paragraph.','past participle':'A verb form used with have or has in the present perfect.','agreement':'Matching a verb form with its subject.'},[
('Choose the past tense of go.',['Went','Goed','Going'],'Went','Go has the irregular past form went.'),
('Complete: She ___ to school every day.',['walks','walk'],'walks','A singular third-person subject takes walks in the simple present.'),
('Correct: Yesterday I write a letter.',None,'Yesterday I wrote a letter.','Use the simple past wrote.'),
('Join with a suitable connector: It rained. We stayed indoors.',None,'It rained, so we stayed indoors.','So expresses a result; because with a reordered sentence is also valid.'),
('Write a topic sentence about reading.',None,'Reading regularly helps students develop vocabulary.','Accept one clear main idea about reading.'),
('Write a three-sentence paragraph about caring for school property.',None,'We should care for school property. Keeping desks clean and returning borrowed books helps everyone. These habits make our school a better place to learn.','One mark each for a main idea, supporting detail and coherent language.')])]
}
lessons=[]; questions=[]; books=[]; glossary=[]
for sid,name,icon,lang in subjects:
 for form in [1,2]:
  title,paragraphs,examples,terms,qs=chapters[sid][form-1]; lid=f'{sid}-f{form}-01'
  lessons.append(dict(id=lid,form=form,subjectId=sid,topicId=lid,title=title,language=lang,objectives=['Explain the key ideas in this chapter.' if lang=='en' else 'Eleza dhana kuu za sura hii.','Apply the ideas to the worked examples and exercises.' if lang=='en' else 'Tumia dhana katika mifano na mazoezi.'],paragraphs=paragraphs,examples=examples,summary=paragraphs[0].split('. ')[0]+'.',glossary=list(terms),diagram='/diagrams/cell.svg' if sid=='biology' and form==1 else '/diagrams/particles.svg' if sid=='chemistry' and form==2 else None,curriculumStatus='provisional-unmapped',publicationStatus='published',completionStatus='starter-chapter'))
  for term,definition in terms.items(): glossary.append(dict(id=f'{lid}-{len(glossary)}',term=term,definition=definition,lessonId=lid))
  for i,(prompt,options,answer,feedback) in enumerate(qs):
   questions.append(dict(id=f'{lid}-q{i+1}',paperId=None,form=form,subjectId=sid,topicIds=[lid],subtopicIds=[lid],sourceType='original',sourceTitle='SomaSmart original practice',institution='SomaSmart',year=None,curriculumEdition='mapping-pending',questionNumber=str(i+1),parentQuestionId=None,type='mcq' if options else 'short',instructions='',content=prompt,options=options or [],media=[],maximumMarks=1 if options else 3 if ('paragraph' in prompt or 'aya fupi' in prompt) else 2,markIncrement=1,answerKey=answer,markingGuide=feedback,solutionProvenance='SomaSmart independently authored',sourceReference='Original authored starter collection',rightsStatus='original',verificationStatus='author-reviewed',publicationStatus='published'))
  for kind in ['textbook','workbook']:
   books.append(dict(id=f'{sid}-f{form}-{kind}',form=form,subjectId=sid,kind=kind,title=f'{name} • Form {form} • '+('Textbook' if kind=='textbook' else 'Revision workbook'),lessonIds=[lid],completionStatus='partial',curriculumVerified=False))
data=dict(version='0.1.0',status='development-partial',subjects=[dict(id=s,name=n,icon=i,language=l) for s,n,i,l in subjects],lessons=lessons,questions=questions,books=books,glossary=glossary,papers=[],curriculum=dict(status='unverified',cohort='Form One 2026 → Form Two 2027',note='Official syllabus editions, teaching languages and transition mapping require verification. These are original starter chapters, not complete textbooks.'))
(root/'content/library.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print(len(lessons),'lessons;',len(questions),'original questions;',len(books),'partial books')
