w_styles = {'NA':'Narrative',
 'IN': 'Informational Description',
 'OP':'Opinion',
 'ID':'Interactive Discussion',
 'HI':'Instruction',
 'IP':'Informational Persuasion',
 'LY':'Lyrical',
 'SP':'Spoken',}



instructions = {'free_style':['Write {n} sentences about {topic} in {style_name} style.',
                             'Write a paragraph about {topic} in {style_name} style.'],
                'fill_word':['Fill in the missing words in the following paragraph: {sent}'],
                'fill_sent':['Fill in the missing sentences knowing that the pargraph follow {style_name} style about {topic}: {sent}',
                            'In {article} {style_name} paragraph about {topic}. What sentence is missing? Please provide the missing sentence following the same strcture: {sent}'],
               'fill_parh':['Fill in the missing paragraph with {n} senteces in the style of {style_name} about {topic}']}

sub_pro = ['I', 'you', 'thy', 'he', 'she', 'it', 'one', 'we', 'you', 'who', 'what', 'well','the', 'is','are' ]


def generate_inst(ex, topic=None):
    
    inst_format = random.choice(list(instructions.keys()))
    masked_sent = ''
    num_sent =  len(re.split(r'[.!?]+', ex['text']) )
    captial = re.findall(r'\b[A-Z]\w*', ex['text']) 
    index = 0
    for j in captial:
        if j.lower() not in sub_pro or len(j) <1:
            captial = j
            index = ex['text'].index(captial)
            break

    if topic == None:
        captialized_words = re.search(r'\b[A-Z]\w*( [A-Z]\w*)*\b', ex['text'][index:])
        topic = captialized_words.group()

    rags = range(len(instructions[inst_format]))
    index = random.choice(rags)

    if inst_format == 'fill_word':
        masked_sent = mask_words(ex['text'])


    elif inst_format == 'fill_sent':
        masked_sent = mask_sentence(ex['text'])
    elif inst_format == 'fill_parh':
        mask_sent = mask_paragraph(ex['text'])
    if ex['labels']:

        style = ex["labels"][0]
        article = get_article(style)
        prompt = instructions[inst_format][index].format(n=num_sent,
                                        topic=topic,
                                        article=article,
                                        style_name=w_styles[style],
                                        sent=masked_sent)
        ex['prompt'] = prompt
    else:
        ex['prompt'] = ''

    return ex
