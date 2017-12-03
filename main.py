from flask import Flask, request
import os
import json
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/', methods=['POST'])
def get_skills():
  input_text = request.data
  os.system('echo {0} | opennlp TokenNameFinder en-ner-skill.bin > outfile.txt'.format(input_text))
  resp = open("outfile.txt", "rt")

  tags = {}

  start_split = resp.read().split('<START:skill>')

  for i in start_split[1:len(start_split)]:
    tag = i.split('<END>')[0]
    tag_dirtylist = tag.split(' ')
    tag_list = []
    for word in tag_dirtylist:
      if word.rstrip():
          tag_list.append(word)
    tags[tag] = tag_list

  return json.dumps(tags)

if __name__ == '__main__':
  app.run(debug=True)
