"""Original distinct revision tasks, separate from textbook activities."""
import pathlib,json
ROOT=pathlib.Path(__file__).resolve().parents[1]
# New-chapter application tasks: five independent answerable items each.
sets={
'chemistry-f1-elements':[
('A label says Co and another says CO. Explain why their meanings differ.','Co is the element cobalt; CO is carbon monoxide, a compound of carbon and oxygen.','Check letter case and whether one or two elements are represented.'),
('A pure substance has particles containing one nitrogen and three hydrogen atoms. Write its formula and total atoms per molecule.','NH₃; four atoms per molecule.','Use element symbols and a subscript for three hydrogen atoms.'),
('Explain why dissolving salt in water is different from forming a new compound.','The components remain a mixture and can be separated physically; a new compound involves chemical joining in a fixed ratio.','Compare mixture formation with chemical combination.'),
('Count atoms of each element in 4CO₂.','Four carbon atoms and eight oxygen atoms.','Multiply every formula count by the coefficient.'),
('A learner puts sodium in a group because of the first letter of its name. Explain the error.','Periodic-table position is based on atomic structure and atomic number, not alphabetical order.','Do not confuse a table group with a naming convention.')],
'chemistry-f2-atoms':[
('An atom has 19 protons, 20 neutrons and 19 electrons. Give Z, A and its shell arrangement.','Z=19, A=39; arrangement 2,8,8,1.','Count protons for Z and add protons and neutrons for A.'),
('A neutral atom has arrangement 2,8,6. State its electron number and period.','16 electrons; period 3.','Add shell populations and count occupied shells.'),
('A magnesium atom loses two electrons. What are its charge and electron arrangement?','Mg²⁺ with arrangement 2,8.','The neutral atom starts with 12 electrons.'),
('Compare chlorine-35 and chlorine-37, both with Z=17.','Both have 17 protons; they have 18 and 20 neutrons respectively.','Changing neutrons makes isotopes, not a different element.'),
('A student states that every atom has equal proton and neutron numbers. Give a counterexample.','Sodium-23 has 11 protons and 12 neutrons.','One valid atom with unequal counts disproves the universal claim.')],
'physics-f1-forces':[
('A 50 N force moves a trolley 8 m in the force direction in 10 s. Find work and average power.','Work=400 J; power=40 W.','Use W=Fs, then P=W/t.'),
('A foot exerts 300 N on 0.015 m². Find the pressure.','20,000 Pa.','Divide normal force by area in m².'),
('A machine receives 800 J and delivers 200 J useful work. Find efficiency and non-useful energy transfer.','25%; 600 J transferred in other ways.','Useful/input ×100%, then subtract useful from input.'),
('Two pupils push a box in opposite directions with equal 40 N forces. Describe the resultant and what it does not tell you.','Resultant is zero; it does not by itself tell whether the box is stationary or moving at constant velocity.','Distinguish force balance from state of motion.'),
('Explain why using a larger supporting area can protect soft ground from a heavy load.','The same normal force distributed over a larger area gives lower pressure.','Connect the area change to F/A.')],
'physics-f2-light':[
('A ray makes 18° with a plane mirror. Calculate incidence and reflection angles.','Both are 72° to the normal.','Subtract 18° from 90°.'),
('A student moves from 1 m to 1.5 m in front of a plane mirror. Find the change in object–image separation.','Separation changes from 2 m to 3 m, an increase of 1 m.','Both object and virtual image distances contribute.'),
('Explain why a glass window may both transmit light and reflect some light.','Different portions of incident light can be transmitted and reflected at its surfaces.','Do not assume transparent means zero reflection.'),
('A ray enters water exactly along the normal. Does the absence of bending prove its speed stays the same?','No. Its speed can change at normal incidence without a direction change.','Separate speed change from bending.'),
('Explain why a mirror image can appear behind an opaque wall-mounted mirror.','Reflected rays reach the eye as if originating behind the mirror; the image is virtual.','No physical object or real ray convergence is required behind it.')],
'biology-f1-photosynthesis':[
('A plant is supplied with more light but its rate stays unchanged. Give two possible limiting factors.','Carbon dioxide availability or temperature; water supply can also limit it.','More light need not overcome a different shortage.'),
('Explain a connection between stomata and the risk of water loss.','Open stomata allow carbon dioxide entry but also permit water vapour to leave.','Show the trade-off between gas exchange and water conservation.'),
('An iodine result is brown rather than blue-black. What can be concluded, and what cannot?','Starch was not detected under the test conditions; this alone does not prove the plant has never photosynthesised.','Distinguish a specific observation from a broad claim.'),
('Design a paper-based comparison to investigate the need for light without doing laboratory work.','Compare supplied starch-test observations from otherwise similar leaves with illuminated and covered regions, checking controls and prior starch conditions.','State the changed factor, controls and evidence to compare.'),
('Explain why nitrates and magnesium cannot replace sunlight in photosynthesis.','They support plant structure and chlorophyll/protein production but do not supply the light energy used by the process.','Distinguish nutrients from energy input.')],
'biology-f2-nutrition':[
('A learner describes bile as a protein-digesting enzyme. Correct both parts.','Bile is not an enzyme; it emulsifies fats and helps neutralise acid. Proteases digest protein.','Correct the identity and function.'),
('Explain why diarrhoea or damaged intestine can affect nutrition even when food is eaten.','Food intake does not guarantee effective absorption of water and nutrients; intestinal function matters.','This is a conceptual answer, not a diagnosis.'),
('Compare the roles of teeth and amylase when eating starchy food.','Teeth mechanically break it up; amylase chemically breaks down starch.','Mention increased surface area as a link.'),
('Plan three headings for a report interpreting supplied food-test results.','Method/conditions, observations/results, and conclusions with limitations.','Observed colour changes should be distinguished from nutrient conclusions.'),
('Why is a meal rich in energy not necessarily balanced?','It may lack adequate protein, vitamins, minerals, fibre or water even if it supplies enough energy.','Adequacy involves different nutrient roles.')],
'mathematics-f1-real-numbers':[
('Convert 0.454545… into a fraction.','5/11.','100x−x=45, so x=45/99=5/11.'),
('Solve −4x ≥ 20.','x ≤ −5.','Reverse the sign when dividing by −4.'),
('Round 0.009965 to three significant figures.','0.00997.','The first significant digit is 9 and the next retained digit rounds up.'),
('Order −3/2, −1.2 and −2 from smallest to largest.','−2, −3/2, −1.2.','Convert −3/2 to −1.5 or use the number line.'),
('Estimate 49.6/0.248 using convenient rounded values, and explain why it is only an estimate.','50/0.25≈200; rounded inputs differ from the originals.','State the approximations used.')],
'mathematics-f2-quadratics':[
('Solve x² + 2x − 15 = 0.','x=3 or −5.','Factor as (x+5)(x−3).'),
('Solve 2x² − 8 = 0.','x=2 or −2.','First obtain x²=4.'),
('Solve x² − 6x + 2 = 0 by completing the square.','x=3 ± √7.','(x−3)²=7.'),
('Simplify (3²)³/3⁴.','3²=9.','Multiply exponents inside the power, then subtract.'),
('Multiply (2 × 10³)(4 × 10⁻⁵) and write standard form.','8 × 10⁻².','Multiply coefficients and add powers of ten.')],
'kiswahili-f1-aina-za-maneno':[
('Changanua kazi za maneno katika Asha mdogo anakimbia haraka.','Asha ni nomino; mdogo kivumishi; anakimbia kitenzi; haraka kielezi.','Kazi itegemee sentensi iliyotolewa.'),
('Unganisha hoja hizi kwa sababu: Tulisoma maktabani. Darasa lilikuwa na kelele.','Tulisoma maktabani kwa sababu darasa lilikuwa na kelele.','Kiunganishi kionyeshe sababu kwa usahihi.'),
('Tunga aya ya sentensi tatu yenye kiunganishi na kielezi.','Tulipanda miti shuleni. Kisha tuliimwagilia kwa uangalifu. Tulishirikiana kwa sababu tulitaka ikue vizuri.','Pima mpangilio, kiunganishi na kielezi katika muktadha.'),
('Tumia yeye bila kufanya msomaji ashindwe kujua anayerejelewa.','Amina amefika. Yeye atatusaidia kupanga vitabu.','Rejea ya kiwakilishi iwe wazi.'),
('Hariri: je amina amemwona juma','Je, Amina amemwona Juma?','Kagua herufi kubwa na alama ya swali.')],
'kiswahili-f2-upatanisho':[
('Geuza kuwa wingi: Mti huu uliopandwa jana umeota.','Miti hii iliyopandwa jana imeota.','Badili nomino, kionyeshi na kirejeshi kwa usahihi.'),
('Geuza kuwa umoja: Vitabu hivi vizuri vimefika.','Kitabu hiki kizuri kimefika.','Vipashio vinavyorejelea nomino vipatane.'),
('Sahihisha na eleza: Watoto hawa amefika mapema.','Watoto hawa wamefika mapema; kitenzi kipatane na watoto.','Usibadili maana bila sababu.'),
('Tunga sentensi changamani kuhusu mwanafunzi na kitabu.','Mwanafunzi aliyekopa kitabu amekirudisha.','Onyesha kishazi tegemezi na upatanisho sahihi.'),
('Eleza kwa mfano kwa nini umbo la nomino pekee halionyeshi wingi kila wakati.','Nyumba imejengwa / nyumba zimejengwa: nomino hubaki ileile lakini kitenzi hubadilika.','Husisha ushahidi na hitimisho.')],
'geography-f1-earth-solar':[
('A is at 20°E and B at 50°E. If A has local solar time 08:00, find B’s.','10:00.','Difference 30° gives 2 hours; B is east and ahead.'),
('Explain why a coordinate written only as 7° is incomplete.','It needs identification as latitude/longitude and a north/south or east/west direction, plus the other coordinate to locate a point fully.','A number alone cannot specify a location.'),
('Compare the causes of day/night and seasons.','Rotation causes day/night; axial tilt with revolution produces the seasonal cycle.','Do not use Sun-distance change as the main seasonal explanation.'),
('Calculate the ideal local-time difference for 7.5° longitude.','30 minutes.','7.5 × 4 minutes per degree.'),
('Why should an ideal longitude answer not automatically be used as a travel clock time?','Actual civil time zones and legal time rules may differ from ideal solar-time calculations.','Identify the model’s limitation.')],
'geography-f2-earth-systems':[
('Explain how loss of vegetation can connect the biosphere and hydrosphere.','Fewer plants can change interception, infiltration and runoff, affecting stream flow and erosion.','Give a process link rather than naming two systems.'),
('Correct: The lithosphere is just another word for the crust.','It includes the crust and rigid uppermost mantle.','Distinguish structural boundaries.'),
('Trace one water molecule through three water-cycle stages.','It evaporates from a lake, condenses in a cloud and returns as precipitation.','Keep stages in a physically possible sequence.'),
('Compare the inner and outer core by state.','Inner core is solid; outer core is liquid.','Do not infer state from temperature alone.'),
('Give an example of a geographical model limitation.','A layered model may not use true thickness scale or show variations within each layer.','Explain what information is simplified.')],
'business-f1-enterprise':[
('A pupil says all people who take large risks are good entrepreneurs. Evaluate the statement.','Good entrepreneurship uses research, planning and affordable tests; large unexamined risks can cause avoidable losses.','Distinguish calculated uncertainty from reckless gambling.'),
('Write two neutral questions to investigate demand for a bicycle repair service.','Where do you currently get repairs? What affects your choice of repairer?','Questions should not pressure respondents into praising the idea.'),
('A trader expects 40 sales but can survive only if at least 35 sell. Give one way to test this assumption before a large purchase.','Use a small trial or reliable customer orders and compare actual sales with the estimate.','Tie the test to demand uncertainty.'),
('Explain why a one-person business can be quick to decide but vulnerable to illness.','One owner can decide without consulting partners, but operations may depend on that person’s time and skills.','Link the same ownership structure to both effects.'),
('Total unit purchase and delivery cost is 1200 and selling price 1450. What remains before other costs?','TSh 250 per unit.','Do not call this final profit without considering other costs.')],
'business-f2-production-capital':[
('Classify harvesting tomatoes, canning them and delivering cans to a shop.','Primary, secondary and tertiary production respectively.','State how each activity adds usefulness.'),
('A loan of 80,000 requires 8 payments of 12,000 plus a 2000 fee. Find total repayment and total finance cost.','Repayment plus fee=98,000; finance cost=18,000.','Include the fee as well as instalments.'),
('Expected stock is 15+24−19 units. A physical count finds 18. Find expected stock and discrepancy.','Expected 20; physical stock is 2 units lower.','Investigate rather than silently inventing a sale.'),
('Explain why credit-funded stock creates both an opportunity and an obligation.','Goods can be sold before payment is due, but the supplier still must be paid under the terms.','Consider cash flow and the risk of unsold goods.'),
('Give one possible cooperative benefit and one issue to check.','Joint purchasing may reduce costs; members should check fees, obligations and governance.','Do not assume every cooperative guarantees a benefit.')],
'historia-f1-jamii-kabla-ukoloni':[
('Tathmini dai: Jamii isiyo na mfalme ilikuwa haina siasa.','Dai si sahihi; mabaraza ya wazee, mifumo ya ukoo au rika ingeweza kupanga mamlaka na maamuzi.','Tofautisha aina za uongozi.'),
('Eleza uhusiano kati ya mazingira na aina za uzalishaji bila kutumia kauli ya watu wote.','Upatikanaji wa maji au malisho ungeathiri kilimo au ufugaji, lakini jamii ingeweza kuchanganya shughuli na kubadilika.','Epuka kufunga watu wote katika shughuli moja.'),
('Pendekeza ushahidi wa kuchunguza teknolojia ya chuma ya eneo fulani.','Zana, mabaki ya tanuru, muktadha wa uchimbaji na simulizi za mafundi vinaweza kulinganishwa.','Vyanzo mbalimbali viunganishwe bila kuharibu urithi.'),
('Eleza manufaa na athari hasi zinazoweza kuandamana na biashara ya mbali.','Kubadilishana bidhaa na maarifa kunaweza kunufaisha, lakini unyonyaji na biashara ya watumwa vilileta madhara makubwa katika baadhi ya mahusiano.','Linganisha athari kwa makundi na vipindi tofauti.'),
('Kwa nini usihamishe kitu cha kale kutoka mahali kilipopatikana bila rekodi?','Muktadha wake unaweza kutoa ushahidi kuhusu matumizi, uhusiano na kipindi; kuondoa kiholela hupoteza taarifa.','Heshimu utaratibu wa utunzaji na utaalamu.')],
'historia-f2-ukoloni-upinzani':[
('Panga: Muungano, uhuru wa Tanganyika, TANU, Mapinduzi ya Zanzibar.','TANU 1954; uhuru wa Tanganyika 1961; Mapinduzi Januari 1964; Muungano Aprili 1964.','Tarehe na mfuatano viendane.'),
('Linganisha upinzani wa silaha na kuondoka eneo lenye masharti ya kazi.','Mbinu hutofautiana lakini zote zinaweza kuonyesha kukataa masharti; ushahidi wa lengo na muktadha unahitajika.','Usihukumu kukubali au kupinga kutokana na vita pekee.'),
('Sahihisha dai: Uhuru wa Zanzibar na Mapinduzi yalikuwa tukio lilelile.','Uhuru ulikuwa 10 Desemba 1963; Mapinduzi yalikuwa 12 Januari 1964.','Tofautisha matukio na tarehe.'),
('Eleza kwa nini sera za kodi zinaweza kubadili maisha ya kiuchumi.','Zinaweza kuhitaji mapato ya fedha na kuathiri namna watu wanavyotumia kazi, ardhi na uzalishaji.','Husisha sera na maamuzi ya jamii kwa ushahidi.'),
('Pendekeza vyanzo viwili vya kuchunguza tukio la upinzani.','Nyaraka za kipindi hicho na simulizi au ushahidi wa maeneo husika, vikilinganishwa kwa muktadha.','Chunguza mtunzi, kusudi na mapungufu ya kila chanzo.')],
'english-f1-grammar-context':[
('Rewrite in the negative: Asha has a bicycle.','Asha does not have a bicycle.','Use does not + base have.'),
('Correct both verbs: Yesterday he buy a book and readed it.','Yesterday he bought a book and read it.','The written past form of read stays read, with different pronunciation.'),
('Write one routine sentence and one sentence about an action happening now.','I walk to school every day. I am reading now.','Use simple present for the routine and progressive for the present action.'),
('Explain why an university is incorrect in ordinary English.','University begins with a consonant /j/ sound, so a university is used.','Article choice follows sound rather than the written vowel alone.'),
('Give a polite request for directions to a library.','Excuse me, could you tell me how to get to the library?','Use a clear destination and appropriate politeness.')],
'english-f2-inference-summary':[
('Give one fact and one inference from the Halima passage, labeling them.','Fact: she had a borrowed dictionary. Inference: revision was a priority for her that morning.','Separate stated evidence from a reasoned conclusion.'),
('Evaluate: Halima had never been to a market in her life.','Unsupported. Her response on one morning does not establish her lifelong behaviour.','Identify the overgeneralisation.'),
('Summarise the passage in no more than twenty words.','Halima revised early at the library, followed her timetable and compared science answers with a friend.','Keep main actions without unsupported additions.'),
('Combine with a result connector: They revised together. They identified different answers to discuss.','They revised together; therefore, they identified different answers to discuss.','Accept a coherent result link; avoid reversing cause and effect.'),
('Paraphrase: Several seats were already occupied.','Other learners were already using a number of seats.','Preserve quantity and meaning without claiming every seat was taken.')]
}
# Distinct tasks for the original eighteen starter chapters.
legacy={
'chemistry-f1-01':[
('A muddy salt solution is filtered. Predict what is in the filtrate.','Water with dissolved salt; much of the insoluble mud is removed.','Filter paper does not remove dissolved salt.'),('Why would a salt-recovery plan use evaporation after filtration?','Filtration removes insoluble material, while evaporation removes solvent and leaves dissolved salt.','Assign the correct function to each stage.'),('Name a separation method when the solvent must also be collected.','Distillation.','Condense the evaporated solvent instead of losing it.')],
'chemistry-f2-01':[
('Explain why gas spreads through a room without the particles becoming larger.','Random particle motion spreads the gas; particle size need not change.','Distinguish distribution from size.'),('A liquid evaporates below its boiling point. Is this a contradiction?','No. Evaporation is a surface process over a range of temperatures.','Boiling and evaporation are different processes.'),('Give a reversible pair of physical state changes.','Melting and freezing.','The chemical identity can stay the same.')],
'physics-f1-01':[
('Mass is 84 g and displacement volume 28 cm³. Find density.','3 g/cm³.','84/28 = 3.'),('A learner reads a cylinder from above at an angle. Identify a likely reading error.','Parallax error.','Place the eye appropriately at the reading.'),('A block is 2 cm by 3 cm by 5 cm and has density 4 g/cm³. Find mass.','120 g.','Volume=30 cm³ and mass=density×volume.')],
'physics-f2-01':[
('A bus travels 2400 m in 4 minutes. Find average speed in m/s.','10 m/s.','Convert 4 minutes to 240 seconds.'),('Compare distance and displacement for one complete lap of a track.','Distance is the lap length; displacement is zero if the start and finish coincide.','Displacement concerns position change.'),('Why cannot two journey speeds always be averaged directly?','The times spent at each speed may differ; use total distance/total elapsed time.','Include any stops in total time.')],
'biology-f1-01':[
('Explain why the presence of a cell wall does not prove a cell photosynthesises.','Many plant cells such as root cells have cell walls but no chloroplasts.','Distinguish wall structure from photosynthetic organelles.'),('Arrange heart, organism, cell and tissue in increasing organisation.','Cell, tissue, heart (organ), organism.','An organ system can occur between organ and organism.'),('Explain why a diagram label should point precisely to a structure.','It makes the intended identification unambiguous and assessable.','Clear drawing conventions support communication.')],
'biology-f2-01':[
('In algae → insect larva → fish, identify the primary consumer.','Insect larva.','It feeds on the producer.'),('Why can removing one predator have more than one effect in a food web?','Species have multiple links and alternative foods, so changes can spread through several relationships.','Avoid an unsupported single guaranteed outcome.'),('Explain why decomposers matter to plant mineral supply.','They break down dead matter and help return nutrients to the environment for plant uptake.','Nutrients cycle, while energy is dissipated.')],
'mathematics-f1-01':[
('Calculate 5/6 − 1/4.','7/12.','Use 10/12 − 3/12.'),('Divide TSh 36,000 in ratio 4:5.','TSh 16,000 and TSh 20,000.','There are nine equal shares.'),('A price of 8000 rises by 12.5%. Find the new price.','TSh 9000.','Increase=1000, then add to the original.')],
'mathematics-f2-01':[
('Solve 7x + 2 = 30.','x=4.','Subtract 2 then divide by 7.'),('Solve 3(x + 4) = 27.','x=5.','Divide by 3 then subtract 4.'),('A number doubled then reduced by 5 is 17. Write and solve an equation.','2x−5=17, so x=11.','Translate the operations in order.')],
'kiswahili-f1-01':[
('Taja tendo la Asha linaloonyesha kushirikisha wengine.','Aliwaomba wenzake wamsaidie kupanga vitabu.','Tumia ushahidi wa kifungu.'),('Andika mrejesho wa heshima kama hukuelewa ujumbe.','Samahani, naomba ufafanue sehemu hii ya ujumbe.','Eleza hitaji bila kukatiza au kudharau.'),('Eleza kwa nini ujumbe unahitaji mahali na wakati sahihi unapomwalika mtu.','Maelezo hayo humsaidia mpokeaji kujua afike wapi na lini.','Ujumbe usio wazi unaweza kusababisha makosa.')],
'kiswahili-f2-01':[
('Tengeneza sentensi ya mada kuhusu michezo shuleni.','Michezo shuleni huchangia afya na ushirikiano wa wanafunzi.','Wazo kuu liwe wazi.'),('Taja hatua mbili kabla ya kuwasilisha aya ya mwisho.','Kuandika rasimu na kuhariri.','Kupanga hoja kabla ya rasimu pia ni muhimu.'),('Unganisha hoja mbili kwa hata hivyo.','Tulipanga kusoma nje; hata hivyo, mvua ilianza kunyesha.','Onyesha tofauti au kizuizi kinachoeleweka.')],
'geography-f1-01':[
('A line measures 6 cm on a 1:50,000 map. Find ground length in km.','3 km.','6×50,000 cm = 300,000 cm.'),('A settlement is south of a lake. State the lake’s direction from the settlement.','North.','Reverse the relative direction.'),('Explain why a map needs a key even if symbols look familiar.','Symbols can differ between maps; the key gives their defined meanings.','Do not assume a symbol has one universal meaning.')],
'geography-f2-01':[
('Daily maximum is 34°C and minimum 21°C. Find range.','13°C.','Subtract minimum from maximum.'),('Why should a missing temperature reading not be entered as 0°C?','It would falsely treat an unobserved value as a real measurement and distort analysis.','Mark it missing.'),('Explain why a thermometer in direct sunshine may misrepresent shaded air temperature.','Solar radiation heats the instrument and can bias its reading.','Use suitable shelter and airflow.')],
'business-f1-01':[
('Income is 18,000, essential spending 12,000 and savings 3000. Find unallocated balance.','TSh 3000.','18,000−12,000−3000.'),('Give an opportunity cost example involving a student’s time.','Choosing revision over the next-best football practice gives up that practice opportunity.','Identify the next best alternative, not all possibilities.'),('Why might a low purchase price hide high total ownership cost?','Repairs, running and maintenance can raise the total over time.','Compare the same period and relevant costs.')],
'business-f2-01':[
('Opening cash is 7000, receipts 11,000 and payments 8500. Find closing cash.','TSh 9500.','7000+11,000−8500.'),('Revenue is 48,000 and all relevant costs total 39,500. Find profit.','TSh 8500.','Subtract costs from revenue.'),('Why can a profitable credit sale leave cash unchanged on the sale date?','The customer has not yet paid, so the sale creates a receivable rather than immediate cash.','Distinguish earning revenue from receiving payment.')],
'historia-f1-01':[
('Mtu aliyetengeneza chanzo alitaka kuwashawishi wasomaji. Kwa nini kusudi hilo lichunguzwe?','Linaweza kuathiri uteuzi na namna ya kuwasilisha taarifa.','Kusudi halifanyi chanzo kisiwe na maana, lakini linahitaji tathmini.'),('Taja tofauti kati ya kumbukumbu ya mshiriki na uchambuzi wa baadaye.','Kumbukumbu inaweza kuwa chanzo cha msingi; uchambuzi wa baadaye hutumia na kutafsiri vyanzo.','Uainishaji hutegemea swali la utafiti.'),('Kwa nini ridhaa ni muhimu katika mahojiano ya historia?','Inaheshimu haki, faragha na masharti ya mtoa taarifa.','Usirekodi bila kukubaliana.')],
'historia-f2-01':[
('Eleza uwajibikaji katika matumizi ya fedha za kikundi.','Kuweka rekodi, kutumia kwa makubaliano na kueleza matumizi kwa wanakikundi.','Unganisha dhamana na kutoa maelezo.'),('Pendekeza njia ya kutatua mgogoro wa matumizi ya vifaa kwa amani.','Sikiliza mahitaji ya pande zote na kubaliana ratiba inayoheshimu haki.','Epuka vitisho na ubaguzi.'),('Kwa nini urithi usio jengo pia unahitaji kutunzwa?','Lugha, maarifa na sanaa vina thamani ya kihistoria na kijamii inayoweza kupotea.','Toa mfano wenye maana.')],
'english-f1-01':[
('What detail shows the seedlings survived and grew?','All three had new leaves two months later.','Use evidence from the original passage.'),('Give an unsupported statement about Neema’s seedlings.','They were mango trees.','The species was not stated.'),('Choose a reading strategy to find the number of seedlings quickly.','Scanning.','Search for the specific numerical detail.')],
'english-f2-01':[
('Correct: Last week they goed to the library.','Last week they went to the library.','Go has the irregular past form went.'),('Write a supporting detail for a paragraph about caring for books.','Returning borrowed books on time lets other students use them.','It must develop the main idea.'),('Combine with because: We used the library. It was quiet.','We used the library because it was quiet.','Express the reason clearly.')]
}
def apply():
 p=ROOT/'content/library.json';d=json.loads(p.read_text());existing={q['id']:i for i,q in enumerate(d['questions'])};added=[]
 for lid,items in {**sets,**legacy}.items():
  l=next(l for l in d['lessons'] if l['id']==lid)
  for i,(prompt,answer,guide) in enumerate(items):
   q=dict(id=f'{lid}-wb-{i+1:02}',paperId=None,form=l['form'],subjectId=l['subjectId'],topicIds=[lid],subtopicIds=[lid],sourceType='original',sourceTitle='SomaSmart original revision workbook',institution='SomaSmart',year=None,curriculumEdition='TIE 2023; coverage partial',questionNumber=str(i+1),parentQuestionId=None,type='short',instructions='',content=prompt,options=[],media=[],maximumMarks=2,markIncrement=1,answerKey=answer,markingGuide=guide+(' Alama 2 kwa jibu na maelezo sahihi; alama 1 kwa uelewa sahihi lakini maelezo pungufu.' if l['language']=='sw' else ' 2 marks for a correct response with required reasoning; 1 for a correct key idea with incomplete reasoning.'),solutionProvenance='SomaSmart independently authored',sourceReference='Original revision workbook batch 2',rightsStatus='original',verificationStatus='author-reviewed',publicationStatus='published',resourceKind='workbook')
   if q['id'] in existing:d['questions'][existing[q['id']]]=q
   else:d['questions'].append(q)
   added.append(q)
 for b in d['books']:
  if b['kind']=='workbook':
   lang=next(s['language'] for s in d['subjects'] if s['id']==b['subjectId'])
   b['introduction']='Jaribu shughuli kabla ya kuangalia majibu. Andika hoja au hatua za hesabu, kisha jitathmini kwa mwongozo.' if lang=='sw' else 'Attempt the revision tasks before opening the model answers. Record your reasoning, then use each rubric to identify what to improve.'
   b['mixedTestQuestionIds']=[q['id'] for q in d['questions'] if q['form']==b['form'] and q['subjectId']==b['subjectId'] and q.get('resourceKind')=='workbook']
 (ROOT/'content/batches/003-workbooks.json').write_text(json.dumps({'questions':added},ensure_ascii=False,indent=2));p.write_text(json.dumps(d,ensure_ascii=False,indent=2));print('Imported',len(added),'distinct workbook activities. Total question bank:',len(d['questions']))
if __name__=='__main__':apply()
