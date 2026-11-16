"""Add original extended responses and structured matching to the starter library."""
import json,pathlib
P=pathlib.Path(__file__).resolve().parents[1]/'content/library.json';d=json.loads(P.read_text());extras={
'chemistry':[
('essay','A pupil says that filtration can produce pure water from salt water. Explain the error and describe a method that can collect the water.','Dissolved salt passes through ordinary filter paper. Simple distillation boils the water, cools its vapour and collects the condensed water separately from the non-volatile salt.','1 mark for explaining dissolved salt passes through; 1 for boiling; 1 for condensing and collecting the water.'),
('short','Compare evaporation and boiling using where they occur and their temperature conditions.','Evaporation occurs at a liquid surface over a range of temperatures. Boiling occurs throughout the liquid at its boiling temperature for the given pressure.','1 mark for surface versus throughout; 1 for temperature conditions; 1 for clear comparison.')],
'physics':[
('calculation','An irregular stone has mass 156 g. A cylinder reads 40 cm³ before immersion and 100 cm³ after. Calculate its density in g/cm³.','Volume = 100 − 40 = 60 cm³. Density = 156/60 = 2.6 g/cm³.','1 mark for volume; 1 for density formula and substitution; 1 for 2.6 g/cm³.'),
('calculation','A learner walks 900 m in 10 minutes, rests for 5 minutes, then walks 600 m in 5 minutes. Find the average speed for the whole journey in m/s.','Distance = 1500 m. Time = 20 min = 1200 s. Average speed = 1500/1200 = 1.25 m/s.','1 mark for total distance; 1 for total time including rest and unit conversion; 1 for correct speed with unit.')],
'biology':[
('matching','Match each cell structure to its main function.',{'membrane':'Regulates movement into and out of the cell','nucleus':'Contains genetic material','chloroplast':'Absorbs light for photosynthesis'},'One mark for each correct structure–function match.'),
('essay','A grassland is converted into a bare parking area. Explain two possible effects on its food web and one conservation response.','Plants and habitats are lost, reducing food or shelter for consumers. Predators may lose prey. Protect remaining habitat or restore native vegetation in an appropriate area.','1 mark for a justified effect on primary consumers; 1 for a linked effect elsewhere in the web; 1 for a relevant conservation action.')],
'mathematics':[
('calculation','A shop reduces a TSh 18,000 bag by 15%. Calculate the discount and the new price.','Discount = 15/100 × 18,000 = TSh 2700. New price = 18,000 − 2700 = TSh 15,300.','1 mark for percent calculation; 1 for discount; 1 for subtracting to obtain the new price.'),
('calculation','Three identical exercise books and a TSh 500 pen cost TSh 5000. Write and solve an equation for the price of one book.','Let x be the price in shillings. 3x + 500 = 5000; 3x = 4500; x = TSh 1500.','1 mark for the equation; 1 for isolating 3x; 1 for the answer with currency.')],
'kiswahili':[
('essay','Kwa kutumia kifungu cha Asha, eleza namna ushirikiano ulivyosaidia darasa. Andika sentensi tatu zenye ushahidi.','Asha aliomba msaada wa wenzake kupanga vitabu. Kwa kushirikiana waliviweka katika sehemu zake. Hivyo wanafunzi walivipata kwa urahisi.','Alama 1 kwa kutaja msaada; 1 kwa kueleza upangaji; 1 kwa kuunganisha matokeo na ushahidi.'),
('essay','Mwandikie rafiki aya fupi ukimweleza umuhimu wa kutunza vitabu. Tumia angalau kiunganishi kimoja kinachofaa.','Vitabu hutusaidia kujifunza, kwa hiyo tunapaswa kuvitunza. Tuvifunike na tuvitumie kwa mikono safi. Pia turudishe vitabu tulivyoazima ili wengine wavitumie.','Alama 1 kwa hoja kuu; 1 kwa maelezo yanayofaa; 1 kwa kiunganishi na mshikamano.')],
'geography':[
('calculation','A straight road is 7 cm long on a 1:25,000 map. Calculate its ground length in metres and kilometres.','7 × 25,000 = 175,000 cm = 1750 m = 1.75 km.','1 mark for applying scale; 1 for metres; 1 for kilometres.'),
('calculation','Rainfall over five observed days is 12, 0, 18, 5 and 0 mm. Find the total and mean daily rainfall for these days.','Total = 35 mm. Mean = 35/5 = 7 mm per day.','1 mark for total; 1 for division by 5 including observed dry days; 1 for mean and unit.')],
'business':[
('essay','A learner can spend one afternoon studying or selling fruit. Explain the opportunity cost of choosing to study, and give one factor that could justify this choice.','If selling fruit was the next best alternative, the benefit forgone from that activity is the opportunity cost. Preparing for an important assessment may justify studying.','1 mark for identifying the next best alternative; 1 for the forgone benefit; 1 for a relevant justification.'),
('calculation','A trader buys and sells all 30 pencils. Each costs TSh 200 and sells for TSh 350. Transport for the batch is TSh 1000. Calculate revenue and profit.','Revenue = 30 × 350 = TSh 10,500. Total cost = 30 × 200 + 1000 = TSh 7000. Profit = TSh 3500.','1 mark for revenue; 1 for total cost; 1 for profit.')],
'historia':[
('essay','Mhojiwa anakumbuka tukio tofauti na barua ya kipindi hicho. Eleza hatua tatu za kuchunguza tofauti hiyo kwa heshima.','Chunguza tarehe na kusudi la barua. Uliza mhojiwa maswali ya ufafanuzi kwa ridhaa yake. Linganisha taarifa zote na vyanzo vingine bila kuficha tofauti.','Alama 1 kwa kuchunguza muktadha; 1 kwa ufafanuzi wenye heshima; 1 kwa ulinganishi wa ushahidi.'),
('essay','Pendekeza mpango wa hatua tatu wa wanafunzi kutunza urithi wa eneo lao bila kuuharibu.','Tambua eneo na wasimamizi wake. Pata ruhusa na ushauri kuhusu kazi salama. Shiriki katika shughuli iliyoruhusiwa na eleza matokeo kwa jamii.','Alama 1 kwa kuhusisha wasimamizi; 1 kwa ruhusa na ushauri; 1 kwa hatua salama na uwajibikaji.')],
'english':[
('essay','Using the Neema passage, write three sentences explaining how the seedlings were cared for. Include two details and a conclusion supported by the passage.','Neema watered the seedlings each evening during the dry week. Her brother protected them from goats with a small fence. Their combined care helped all three seedlings develop new leaves.','1 mark for watering detail; 1 for protection detail; 1 for a supported conclusion in coherent language.'),
('essay','Write a four-sentence paragraph about a completed visit to a library. Include a clear main idea, two supporting details and consistent past tense.','Our class visited the library last Friday. We read short stories and looked up unfamiliar words. The librarian showed us how to find science books. The visit helped us discover useful learning resources.','1 mark for a clear main idea; 1 for relevant supporting details; 1 for consistent tense and coherent sentences.')]
}
for sid,entries in extras.items():
 for form,(kind,prompt,answer,guide) in enumerate(entries,1):
  lid=f'{sid}-f{form}-01';base=next(q for q in d['questions'] if q['topicIds']==[lid]);q={**base,'id':f'{lid}-extended','type':kind,'content':prompt,'options':[],'answerKey':answer,'maximumMarks':3,'markingGuide':guide,'questionNumber':'7'}
  if kind=='matching':q['pairs']=[{'id':k,'left':k.title()} for k in answer];q['options']=list(answer.values())
  if not any(x['id']==q['id'] for x in d['questions']):d['questions'].append(q)
P.write_text(json.dumps(d,ensure_ascii=False,indent=2));print('Original questions:',len(d['questions']))
