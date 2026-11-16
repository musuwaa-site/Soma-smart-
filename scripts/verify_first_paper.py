"""Publish a visually transcribed and independently solved selection from a real paper.
Source cover/questions were inspected as page renders. Owner permission is recorded.
Whole main questions retain their source maximum of 10; own rubric is explicitly labelled.
"""
import pathlib,json,shutil,hashlib,fitz
ROOT=pathlib.Path(__file__).resolve().parents[1];paper_id='necta-ftna-2025-mathematics-200032d2d5376daf';folder=ROOT/'acquisition/documents/200032d2d5376daf'
if not (folder/'original.pdf').exists():folder=ROOT/'public/past-papers'/paper_id
meta=json.loads((folder/'source.json').read_text()) if (folder/'source.json').exists() else next(m for m in json.loads((ROOT/'acquisition/source-register.json').read_text()) if m['id']=='200032d2d5376daf')
assert hashlib.sha256((folder/'original.pdf').read_bytes()).hexdigest()==meta['sha256'],'Source changed: repeat source-page review before publishing.'
assert meta['rightsStatus']=='cleared' and meta.get('rightsEvidence'),'Owner permission must be recorded.'
doc=fitz.open(folder/'original.pdf');D=json.loads((ROOT/'content/library.json').read_text());out=ROOT/'public/past-papers'/paper_id;out.mkdir(parents=True,exist_ok=True)
if (folder/'original.pdf').resolve()!=(out/'original.pdf').resolve():shutil.copyfile(folder/'original.pdf',out/'original.pdf')
for n in [1,2,4,5,6,7,8,9,10,11]:doc[n-1].get_pixmap(matrix=fitz.Matrix(1.15,1.15)).save(out/f'page-{n}.png')
# Original diagrams preserved as crops from the already inspected source pages.
for page_number,name,box in [(5,'q4-angles.png',(0.1,0.14,0.75,0.45)),(10,'q9-triangle.png',(0.12,0.54,0.85,0.82))]:
 page=doc[page_number-1];w,h=page.rect.width,page.rect.height;page.get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(box[0]*w,box[1]*h,box[2]*w,box[3]*h)).save(out/name)
base_path='/past-papers/'+paper_id
# Three concise supplemental revision chapters locate legacy skills without calling them new official subtopics.
bridges=[
('mathematics-f2-number-revision','Number skills: prerequisite revision',[
'Legacy Form Two papers can revisit number skills now introduced earlier in the curriculum. This supplemental revision chapter supports arithmetic, approximation, ratio and percentages. It does not add a new official Form Two syllabus requirement or claim complete curriculum coverage.',
'Evaluate brackets first, then powers, multiplication and division at the same precedence from left to right, then addition and subtraction from left to right. The word of in a fraction expression means multiplication. Keep the sign of a bracketed result: multiplying a positive fraction by a negative number gives a negative result.',
'For rounding to thousands, compare the remainder after complete thousands with 500. For a percentage loss, use loss divided by the original cost price, then multiply by 100%. In a ratio division, add the ratio terms to find the total number of equal shares before multiplying by the required term.'],['(20 ÷ 4 + 3) − 10 = 8 − 10 = −2; one half of this is −1.','A total of 78,650 rounded to the nearest thousand is 79,000 because the final 650 is at least 500.','Divide 24 kg in ratio 1:2:3: total terms 6, one share 4 kg; the largest share is 12 kg.']),
('mathematics-f2-geometry-review','Angles and algebra: prerequisite revision',[
'This supplemental chapter revisits parallel-line angle reasoning and elementary algebra used in legacy examination questions. Use the original diagram when identifying an angle: labels and marked right angles are part of the mathematical information, not decoration.',
'Vertically opposite angles are equal. Angles on a straight line sum to 180°. A transversal crossing parallel lines creates equal corresponding angles and equal alternate angles. Name the angle relationship before inserting a value; a visual estimate of a drawing is not a proof.',
'For a perimeter problem, add all side expressions, equate the sum to the stated perimeter and solve. For expressions, distribute a negative multiplier across every bracket term before collecting like terms. Check numerical solutions in the original conditions, including whether proposed side lengths can form a triangle.'],['An angle adjacent on a straight line to 65° is 180°−65°=115°; its vertically opposite partner is also 115°.','If triangle sides are x+1, x+3 and 6 with perimeter 18, then 2x+10=18, x=4 and the sides are 5,7,6.','4p−2(3q−p)=4p−6q+2p=6p−6q.']),
('mathematics-f2-coordinate-review','Straight lines: prerequisite revision',[
'Legacy assessment questions on coordinate geometry are provided as labelled prerequisite revision. A line y=mx+c has gradient m and vertical-axis intercept c. The intercept is the value of y when x=0; it is not necessarily the constant appearing in an unsimplified equation.',
'If an equation is ky=kx+x+d, first consider k=0 separately. When that case is incompatible with a stated finite gradient, divide by nonzero k to obtain y=((k+1)/k)x+d/k. Only then compare its coefficients with y=mx+c.',
'A line containing a stated point must satisfy its equation when the coordinates are substituted. Two points can provide two equations in unknown coefficients. Solve simultaneously, then verify both original point conditions. Keep negative coordinates and signs intact when substituting.'],['For 2y=6x+8, divide by 2: y=3x+4. The gradient is 3 and y-intercept is 4.','If y=mx+2 passes through (3,8), then 8=3m+2 and m=2.','The line y=2x−1 contains (0,−1) and (2,3), because both substitutions satisfy the equation.'])]
for id,title,paras,examples in bridges:
 if not any(l['id']==id for l in D['lessons']):D['lessons'].append(dict(id=id,form=2,subjectId='mathematics',topicId=id,title=title,language='en',objectives=['Review compatible prerequisite skills.','Use the original source question and independent solution carefully.'],paragraphs=paras,examples=examples,summary=paras[0],glossary=[],diagram=None,curriculumStatus='supplemental-legacy-prerequisite',publicationStatus='published',completionStatus='supplemental-revision'))
rows=[
(1,[2],['mathematics-f2-number-revision'],[
('a','Evaluate 1/5 of ((50 ÷ 5 + 5) − (8 × 4 − 2)).'),
('b','The population of three towns are 65600, 13400 and 29700 to the nearest hundreds. Approximate the total population of the three towns to the nearest thousands.')],
'(a) −3. (b) Approximately 109,000 people.',
'(a) 50÷5=10; 10+5=15; 8×4−2=30; 15−30=−15; (1/5)×(−15)=−3. (b) 65,600+13,400+29,700=108,700; rounding to thousands gives 109,000.',
'(a) Five marks: division 10; first bracket 15; second bracket 30; difference −15; final −3 (one each). (b) Five marks: first sum 79,000; full sum 108,700; identify rounding to thousands; apply the ≥500 rule; give 109,000 people (one each).'),
(3,[4],['mathematics-f2-number-revision'],[
('a','A text book was bought at shs. 8,500 and then sold at shs. 6,000. Calculate the percentage loss.'),
('b(i)','Four families A, B, C and D have to share 33 kilograms of meat in the ratio 4:5:6:7 respectively. What is the largest share?'),
('b(ii)','Which family will get the largest share?')],
'(a) 500/17% ≈ 29.41%. (b)(i) 10.5 kg. (ii) Family D.',
'(a) Loss=8500−6000=2500; percentage loss=(2500/8500)×100=500/17%. (b) Total ratio=22; one share=33/22=1.5 kg; largest term is 7, so 7×1.5=10.5 kg for family D.',
'(a) Five marks: identify original cost; calculate loss 2500; divide loss by original cost; multiply by 100; give a valid exact or rounded percentage (one each). (b) Five marks: ratio sum 22; unit share 1.5; identify largest term 7; mass 10.5 kg; family D (one each).'),
(4,[5,6],['mathematics-f2-geometry-review'],[
('a','In the following figure, AB is parallel to PQ and RS is a transversal. Find the angles marked a, b, w, x, y and z.'),
('b','The perimeter of triangle ABC is 16 cm. If the lengths AB=(5+x) cm, AC=(2+x) cm and BC=5 cm, find the value of x and hence the actual lengths of AB and AC.')],
'(a) a=60°, b=120°, w=120°, x=60°, y=120°, z=60°. (b) x=2; AB=7 cm; AC=4 cm.',
'(a) Use vertically opposite angles and straight-line sums; corresponding angles agree across the parallel lines. (b) (5+x)+(2+x)+5=16; 2x+12=16; x=2. Hence AB=7 cm and AC=4 cm.',
'(a) Six marks, one for each correct labelled angle. (b) Four marks: correct perimeter equation; x=2; AB=7 cm; AC=4 cm (one each).'),
(5,[6,7],['mathematics-f2-geometry-review','mathematics-f2-quadratics'],[
('a(i)','Simplify 7m − 2(5n − 4m) + 11n − 5m.'),
('a(ii)','Simplify (5x − 2y) − 2(4x − 3y).'),
('b','The sum of two numbers is 19 and their difference is 5. Find the numbers.')],
'(a)(i) 10m+n. (ii) −3x+4y. (b) 12 and 7.',
'(i) 7m−10n+8m+11n−5m=10m+n. (ii) 5x−2y−8x+6y=−3x+4y. (b) Let u+v=19 and u−v=5; adding gives 2u=24, so u=12 and v=7.',
'(a) Three marks per expression: distribute to each bracket term correctly (two marks), then collect correctly (one mark). (b) Four marks: sum equation; difference equation; elimination/substitution step; both correct numbers (one each).'),
(6,[7,8],['mathematics-f2-coordinate-review'],[
('a(i)','The gradient of the line ky=kx+x+7 is 2. Find the value of k.'),
('a(ii)','Write down its y-intercept.'),
('b','The graph of straight line Kx−My−4=0 passes through the points A(−2,−5) and B(2,−3). Find the values of K and M.')],
'(a)(i) k=1. (ii) y-intercept=7. (b) K=1/2, M=1.',
'(a) For k≠0, y=((k+1)/k)x+7/k. Set (k+1)/k=2, giving k=1 and intercept 7. k=0 gives a vertical condition rather than the stated finite gradient. (b) −2K+5M=4 and 2K+3M=4; addition gives M=1, then K=1/2. Both source points satisfy the resulting line.',
'(a) Five marks: rearranged slope form; correct gradient equation; solve k=1; identify intercept expression 7/k; obtain intercept 7 (one each). (b) Five marks: substitute A; substitute B; solve M=1; solve K=1/2; verify both points (one each).'),
(7,[8,9],['mathematics-f2-quadratics'],[
('a','Find the value of 8^(−2/3) + (3^(−2))/(2^(−3)).'),
('b','Rationalize the denominator of √2/(√3+√2).')],
'(a) 41/36. (b) √6−2.',
'(a) 8^(−2/3)=1/4 and (3^−2)/(2^−3)=(1/9)/(1/8)=8/9. Sum=9/36+32/36=41/36. (b) Multiply numerator and denominator by √3−√2: (√6−2)/(3−2)=√6−2.',
'(a) Five marks: cube root of 8 is 2; first term 1/4; 3^−2=1/9; quotient term 8/9; correct sum 41/36 (one each). (b) Five marks: choose conjugate; multiply numerator; evaluate denominator as 3−2; simplify denominator to 1; obtain √6−2 with valid working (one each).'),
(9,[10,11],['mathematics-f2-sets-trigonometry'],[
('a','Calculate the length y in the following figure. Give the correct answer to one decimal place.'),
('b(i)','A ladder on the ground leans against a vertical wall whose height is 5 metres. The ground distance between the ladder and the wall is 12 metres. Draw a diagram to represent this information.'),
('b(ii)','By using the diagram in part (b)(i), find the length of the ladder.')],
'(a) y=28.2 cm. (b) A right triangle with vertical side 5 m, horizontal side 12 m and ladder as hypotenuse; ladder=13 m.',
'(a) sin70°=y/30, so y=30sin70°≈28.1908 cm, giving 28.2 cm. (b) Interpreting the ladder as reaching the stated 5 m height, L²=5²+12²=169, so L=13 m. The wall and ground are perpendicular as the stated vertical/ground model requires.',
'(a) Five marks: identify opposite side; sine ratio; rearrange to y=30sin70°; correct numerical evaluation; rounding and cm (one each). (b) Five marks: correctly labelled right-triangle sketch; Pythagorean equation; sum 169; square root 13; metres and interpretation of the sketch (one each).')]
questions=[]
for number,pages,topics,parts,answer,solution,rubric in rows:
 id=paper_id+f'-q{number}';content='\n\n'.join(f'({label}) {text}' for label,text in parts);media=[]
 if number in [4,9]:media.append({'path':base_path+('/q4-angles.png' if number==4 else '/q9-triangle.png'),'alt':'Original source angle diagram, labels and given 120°/60° angles.' if number==4 else 'Original right triangle: hypotenuse 30 cm, angle 70°, and opposite length y.','role':'diagram'})
 for page in pages:media.append({'path':base_path+f'/page-{page}.png','alt':f'Original source page {page}, preserving printed wording, figures and units.','role':'source-page'})
 questions.append(dict(id=id,paperId=paper_id,form=2,subjectId='mathematics',topicIds=topics,subtopicIds=topics,sourceType='necta',sourceTitle='NECTA FTNA 2025 • Basic Mathematics • reviewed selection',institution='National Examinations Council of Tanzania (source cover)',year=2025,curriculumEdition='Legacy 2025 paper; compatible current topics or clearly labelled prerequisite revision only',questionNumber=str(number),parentQuestionId=None,type='calculation',instructions='Keep all linked subparts together. Write labelled working for every part. The source allocates 10 marks to the whole main question. Written scoring uses independent SomaSmart guidance, not an official NECTA marking scheme.',content=content,subquestions=[{'id':id+'-'+label.replace('(','').replace(')',''),'label':label,'content':text,'parentQuestionId':id} for label,text in parts],options=[],media=media,maximumMarks=10,markIncrement=1,marksProvenance='Source PDF page 1, instruction 3: each question carries ten (10) marks.',markIncrementProvenance='Independent whole-mark self-assessment rubric; official subpart weights are not asserted.',answerKey=answer,markingGuide='Independent SomaSmart self-assessment rubric (not an official NECTA scheme). '+rubric+' Accept valid equivalent methods and apply reasonable follow-through without double-penalising one arithmetic slip.',workedSolution=solution,solutionProvenance='Independently prepared and calculation-checked by SomaSmart; no official answer key claimed.',sourceReference=meta['url'],sourcePdf=base_path+'/original.pdf',sourcePages=pages,sourceSha256=meta['sha256'],rightsStatus='cleared',rightsEvidence=meta['rightsEvidence'],verificationStatus='verified',verificationScope='Wording compared visually with source-page images; numbers/formulae/diagrams retained; independent solutions checked. Archive attribution checked against the printed cover, not separately certified by NECTA.',publicationStatus='published',resourceKind='past-paper'))
existing={q['id']:i for i,q in enumerate(D['questions'])}
for q in questions:
 if q['id'] in existing:D['questions'][existing[q['id']]]=q
 else:D['questions'].append(q)
paper=dict(id=paper_id,title='NECTA FTNA 2025 • Basic Mathematics • reviewed selection',form=2,subjectId='mathematics',sourceType='necta',institution='National Examinations Council of Tanzania (source cover)',year=2025,sourceReference=meta['url'],sourcePdf=base_path+'/original.pdf',sourceSha256=meta['sha256'],rightsStatus='cleared',rightsEvidence=meta['rightsEvidence'],verificationStatus='verified',verificationScope='Only the listed selected main questions, not the entire paper.',publicationStatus='published',publicationScope='selected-questions',completePaper=False,questionIds=[q['id'] for q in questions],maximumMarks=70,sourceInstructions=['This paper consists of ten (10) questions.','Answer all questions.','Each question carries ten (10) marks.','Show clearly all the working and answers in the space provided.','All writing must be in blue or black ink, except drawings which must be in pencil.','NECTA mathematical tables, geometric instruments and graph papers may be used where necessary.','Communication devices, calculators and any unauthorised materials are not allowed in the assessment room.','Write your Assessment Number at the top right corner of every page.'],excludedQuestions=[{'number':'2','reason':'Part (a) omits whether tea/coffee sets overlap. Six drink tea and five coffee; number drinking neither can range from four to nine. Do not silently assume mutual exclusion.'},{'number':'8','reason':'Part (a) prints a triangle similarity ordering that conflicts with the marked right-angle correspondence. Hold the full linked question for editorial review.'},{'number':'10','reason':'Transcription/data and current-curriculum mapping review pending for the entire linked statistics question.'}])
idx=next((i for i,p in enumerate(D['papers']) if p['id']==paper_id),None)
if idx is None:D['papers'].append(paper)
else:D['papers'][idx]=paper
for b in D['books']:
 if b['form']==2 and b['subjectId']=='mathematics':b['lessonIds']=[l['id'] for l in D['lessons'] if l['form']==2 and l['subjectId']=='mathematics']
D['version']='0.3.1';(ROOT/'content/library.json').write_text(json.dumps(D,ensure_ascii=False,indent=2));(ROOT/'content/batches/007-reviewed-authentic-selection.json').write_text(json.dumps({'papers':[paper],'questions':questions},ensure_ascii=False,indent=2));print('Published 7 source-traceable main question groups containing 18 labelled answerable parts, with source images and independently checked solutions.')
