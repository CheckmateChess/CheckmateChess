from django.shortcuts import render
from socket import *
from json import *

from checkmateclient.forms import startForm, connectForm,hiddenForm, playForm, depthForm,modeForm




# Create your views here.

def home(request):
    return render(request, 'index.html')


def start(request):
    form = startForm()
    context = {'form': form}
    return render(request, 'start.html', context)


def connect(request):
    form = connectForm()
    context = {'form': form}
    return render(request, 'connect.html', context)


def upload_book(book):
    with open('checkmateclient/books/%s' % book.name, "wb+") as f:
        for chunk in book.chunks():
            f.write(chunk)


def play(request):

    print '-----------------------------------------------------------------'
    print request.POST
    print '-----------------------------------------------------------------'


    data = request.POST

    if not data:
        return render(request, 'play.html', {})

    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("0.0.0.0", 20001))

    if data['operation'] == 'Start':
        if request.FILES.get('book'):
            upload_book(request.FILES.get('book'))

        s.send('{"op":"start" , "color":"%s","params":["%s","%s","%s"]}' % (
            data.get('color'), data.get('mode'), data.get('difficulty'),
            request.FILES.get('book') and request.FILES.get('book').name ))
        gameid = loads(s.recv(4096)).get('gameid')
        color = data.get('color')
        mode = data.get('mode')
    else:
        gameid = data.get('gameid')
        color = data.get('color')

        s.send('{"op":"connect" , "color":"%s", "gameid":"%s"}' % (data.get('color'), data.get('gameid')))
        s.recv(4096)

        if data['operation'] == 'Play':
            moves = data.get('moves')
            s.send('{"op":"play" , "params":["nextmove","%s","%s"]}' % ( color, moves[:2]+' '+moves[2:] ))
            s.recv(4096)
        elif data['operation'] == 'setDepth':
            depth = data.get('depth')
            s.send('{"op":"play" , "params":["setdepth","%s"]}' % depth)
            s.recv(4096)
        elif data['operation'] == 'changeMode':
            mode = data.get('mode')



    # s.send('{"op":"play","params":["getbookmode"]}')
    #bookmode = loads(s.recv(4096))['bookmode']

    s.send('{"op":"play","params":["getmode"]}')
    mode = loads(s.recv(4096))['mode']

    s.send('{"op":"play","params":["history"]}')
    historyx = loads(s.recv(4096))['history']
    history = []
    for i in range(len(historyx['Black'])):
        history.append( [ historyx['White'][i] ,  historyx['Black'][i] ] )
    if len(historyx['White']) > len(historyx['Black']):
        history.append( [ historyx['White'][-1] ,  ''] )

    s.send('{"op":"play","params":["getdepth"]}')
    depth = loads(s.recv(4096))['depth'] or 10

    s.send('{"op":"play","params":["getboard"]}')
    board = loads(s.recv(4096))['board']
    for i in range(8):
        for j in range(8):
            board[i][j] = [board[i][j], chr(j + ord('a')) + str(8 - i)]

    s.send('{"op":"exit"}')
    s.recv(4096)

    s.close()

    context = { 'hiddenForm': hiddenForm(initial={'gameid':gameid,'color':color}),
                'playForm' : playForm(),
                'board': board,
                'depthForm': depthForm(initial={'depth': int(depth)}),
                'history':history,
                'modeForm':modeForm(inital={'mode':mode}),
               #'bookmodeform': bookmodeForm(initial={'bookmode':bookmode})
    }

    return render(request, 'play.html', context)
