from datasets import load_dataset
import re
import random

def mask_words(text):
    text = text.split()
    num_mask = random.choice()
    index = random.choice(range(len(text)))
    text[index] = '....'
    
import random

def mask_words(sentence, prob_mask=0.1):
    """Randomly replace words in a sentence based on
    a given probability.
    args:
        sentence (str): The sentence to be replace with ...
        prob_mask (float): The probability of a word being masked.
    Returns:
        str: The sentence with the masked words.
    """
    words = sentence.split(' ')
    n = round(len(words) * prob_mask)
    maskedw = ['The missing words:']
    for i in random.sample(range(len(words)), n):
        maskedw.append(f'{words[i]},')
        words[i] = '...'
    
    maskedw[-1] = maskedw[-1].replace(',','')
    merged_words = []
    for word in words:
        if word == '*':
            if merged_words and merged_words[-1] == '*':
                continue
            merged_words.append('*')
        else:
            merged_words.append(word)
    
    return ' '.join(merged_words)      



def mask_sentence(sentence, prob_mask=0.1):
    """
    """
    words = sentence.split('.')
    n = round(len(words) * prob_mask)
    masked_sen = []
    for i in random.sample(range(len(words)), n):
        masked_sen.append(words[i])
        words[i] = '...'
    
    merged_words = []
    for word in words:
        if word == '*':
            if merged_words and merged_words[-1] == '*':
                continue
            merged_words.append('*')
        else:
            merged_words.append(word)
    return ' '.join(merged_words)     



def mask_paragraph(sentence):
    """
    """
    words = sentence.split('\n')[:-1]
    
    i = random.sample(range(len(words)),1)[0]
    missing = words[i]
    words[i] = '...'
    
    return ' '.join(words),missing

   
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


def get_article(word):
    vowels = ['a', 'e', 'i', 'o', 'u']
    if word[0].lower() in vowels:
        return 'an'
    else:
        return 'a'
     
     

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

   
ds = load_dataset('TurkuNLP/register_oscar','en',cache_dir='/media/khalid/data_disk/cache_dataset/TurkuNLP/')
ds = ds.map(generate_inst)
ds.to_json('oscar.json',
          orient = 'records',
          lines=True,)
