# This file is part of Checkmate. 
# 
# This program is free software: you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License 
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# Copyright 2015 Ozge Lule(ozge.lule@ceng.metu.edu.tr), 
#                Esref Ozturk(esref.ozturk@ceng.metu.edu.tr)


from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from socket import *
from json import *
import os.path

from checkmateclient.forms import *

HOST = '0.0.0.0'
PORT = 20000








# Create your views here.

def handlepost(request):
    pass

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


def upload_book(book, gameid=0):
    bookname = book.name
    if gameid:
        bookname = str(gameid) + ".pgn"
    with open('checkmateclient/books/%s' % bookname, "wb+") as f:
        for chunk in book.chunks():
            f.write(chunk)

def editboard(board):
    for i in range(8):
        for j in range(8):
            board[i][j] = [board[i][j], chr(j + ord('a')) + str(8 - i)]
    return board

def play(request):

    cookie = request.COOKIES
    data = request.POST

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((HOST, PORT))


    if  data.get('operation') == 'book':
        upload_book(request.FILES['book'])
        s.send('{"op":"connect" , "color":"%s", "gameid":"%s"}' % (cookie['color'], cookie['gameid']))
        response = loads(s.recv(4096))
        gameid = cookie['gameid']
        color = cookie['color']
        board = editboard(response['board'])
        s.send('{"op":"play" , "params":["addbook","%s/books/%s"]}' % (
                    os.path.dirname(os.path.realpath(__file__)), request.FILES.get('book').name))
        s.recv(4096)

    elif cookie.get('gameid') and cookie.get('color'):
        s.send('{"op":"connect" , "color":"%s", "gameid":"%s"}' % (cookie['color'], cookie['gameid']))
        response = loads(s.recv(4096))
        if not response['success']:
            return HttpResponse('<h1 style:"align:center" > Could not connect to game with id=%d</h1>' % cookie['gameid'] )
        gameid = cookie['gameid']
        color = cookie['color']
        board = editboard(response['board'])
    elif data.get('operation') == 'Start':
        s.send('{"op":"start" , "color":"%s","params":["%s","%s","%s"]}' % (
                data['color'], data['mode'], data['difficulty'],
                None ))
        response = loads(s.recv(4096))
        gameid = response['gameid']
        color = data['color']
        board = editboard(response['board'])
    elif data.get('operation') == 'Connect':
        s.send('{"op":"connect" , "color":"%s", "gameid":"%s"}' % (data['color'], data['gameid']))
        response = loads(s.recv(4096))
        if not response['success']:
            return HttpResponse('<h1 style:"align:center" > Could not connect to game with id=%d</h1>' % cookie['gameid'] )
        gameid = data['gameid']
        color = data['color']
        board = editboard(response['board'])


    s.send('{"op":"exit"}')
    s.recv(4096)
    s.close()

    context = { 'gameid':gameid,
                'board':board,
                'color':color,
                'depth':3,
                'enablebook':'disabled',
                'bookmode':'random',
                'bookForm':bookForm(),
    }


    response = render(request, 'play.html', context)
    response.set_cookie("gameid", str(gameid))
    response.set_cookie("color",str(color))
    return response

def handlepost(request):

    data = request.GET
    if not data:
        return HttpResponse("Noooooo")
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send('{"op":"connect" , "color":"%s", "gameid":"%s"}' % (data['color'], data['gameid']))
    s.recv(4096)
    query = loads(data['query']);
    if query.get('params') and 'save' in query.get('params'):
        query.get('params')[1] = os.path.dirname(os.path.realpath(__file__)) + '/saved/' + query.get('params')[1] + '.pgn';
    if query.get('params') and 'load' in query.get('params'):
        query.get('params')[1] = os.path.dirname(os.path.realpath(__file__)) + '/saved/' + query.get('params')[1] + '.pgn';
    s.send(dumps(query))
    response = s.recv(4096)
    s.send('{"op":"exit"}')
    s.recv(4096)
    s.close()

    return HttpResponse(response)


def play2(request):
    data = request.POST
    hintFormx = None

    # if not data:
    #    return render(request, 'play.html', {})

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((HOST, PORT))

    if data:
        if data['operation'] == 'Start':
            bookname = None

            s.send('{"op":"start" , "color":"%s","params":["%s","%s","%s"]}' % (
                data.get('color'), data.get('mode'), data.get('difficulty'),
                bookname ))
            gameid = loads(s.recv(4096)).get('gameid')
            color = data.get('color')
            mode = data.get('mode')
            enablebook = False

            context = {'hiddenForm': hiddenForm(initial={'gameid': gameid, 'color': color, 'bookenabled': enablebook}),
                       'gameid': gameid

            }

            return render(request, 'showgameid.html', context)

        else:
            gameid = data.get('gameid')
            color = data.get('color')
            enablebook = data.get('bookenabled') == 'enabled'

            s.send('{"op":"connect" , "color":"%s", "gameid":"%s"}' % (data.get('color'), data.get('gameid')))
            s.recv(4096)

            if data['operation'] == 'Play':
                moves = data.get('moves')
                s.send('{"op":"play" , "params":["nextmove","%s","%s"]}' % ( color, moves[:2] + ' ' + moves[2:] ))
                feedback = loads(s.recv(4096))
                if feedback.get('message') == 'Game is killed':
                    s.close()
                    return HttpResponseRedirect("/../killed")
                elif feedback.get('isfinished'):
                    s.close()
                    return HttpResponseRedirect("/../finished?winner=%s" % color)

            elif data['operation'] == 'setDepth':
                depth = data.get('depth')
                s.send('{"op":"play" , "params":["setdepth","%s"]}' % depth)
                s.recv(4096)
            elif data['operation'] == 'changeMode':
                mode = data.get('mode')
                s.send('{"op":"play" , "params":["changemode","%s"]}' % mode)
                s.recv(4096)
            elif data['operation'] == 'newgame':
                s.send('{"op":"play" , "params":["newgame"]}')
                s.recv(4096)
            elif data['operation'] == 'addbook':
                upload_book(request.FILES.get('book'))
                s.send('{"op":"play" , "params":["addbook","%s/books/%s"]}' % (
                    os.path.dirname(os.path.realpath(__file__)), request.FILES.get('book').name))
                s.recv(4096)
            elif data['operation'] == 'enablebook':
                enablebook = False
                if data.get('enablebook') == 'enabled':
                    enablebook = True
                s.send('{"op":"play" , "params":["enablebook","%s"]}' % enablebook)
                s.recv(4096)
            elif data['operation'] == 'setbookmode':
                s.send('{"op":"play" , "params":["setbookmode","%s"]}' % data.get('bookmode'))
                s.recv(4096)
            elif data['operation'] == 'undo':
                s.send('{"op":"play" , "params":["undo"]}')
                s.recv(4096)
            elif data['operation'] == 'save':
                s.send('{"op":"play" , "params":["save","%s/saved/%s.pgn"]}' % (
                    os.path.dirname(os.path.realpath(__file__)), data.get('savefile')))
                s.recv(4096)
            elif data['operation'] == 'load':
                if os.path.isfile("%s/saved/%s.pgn" % (
                        os.path.dirname(os.path.realpath(__file__)), data.get('loadfile'))):
                    s.send('{"op":"play" , "params":["load","%s/saved/%s.pgn"]}' % (
                        os.path.dirname(os.path.realpath(__file__)), data.get('loadfile')))
                    s.recv(4096)
            elif data['operation'] == 'hint':
                s.send('{"op":"play" , "params":["hint"]}')

                hintFormx = hintForm(initial={'hint': loads(s.recv(4096)).get('hint')})

            elif data['operation'] == 'exit':
                s.send('{"op":"exit"}')
                s.recv(4096)
                s.close()
                return HttpResponseRedirect("/../")
            elif data['operation'] == 'giveup':
                s.send('{"op":"kill"}')
                s.recv(4096)
                s.close()
                return HttpResponseRedirect("/../")

    s.send('{"op":"play" , "params":["isfinished"]}')
    feedback = loads(s.recv(4096))
    if feedback.get('message') == 'Game is killed':
        s.close()
        return HttpResponseRedirect("/../killed")
    elif feedback.get('isfinished'):
        s.send('{"op":"play" , "params":["getwinner"]}')
        winner = loads(s.recv(4096)).get('winner')
        s.close()
        return HttpResponseRedirect("/../finished?winner=%s" % winner)

    s.send('{"op":"play","params":["getbookmode"]}')
    bookmode = loads(s.recv(4096))['bookmode'] or 'random'

    s.send('{"op":"play","params":["getmode"]}')
    mode = loads(s.recv(4096))['mode']

    s.send('{"op":"play","params":["history"]}')
    historyx = loads(s.recv(4096))['history']
    history = []
    for i in range(len(historyx['Black'])):
        history.append([historyx['White'][i], historyx['Black'][i]])
    if len(historyx['White']) > len(historyx['Black']):
        history.append([historyx['White'][-1], ''])

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

    if enablebook:
        enablebook = 'enabled'
    else:
        enablebook = 'disabled'

    context = {'hiddenForm': hiddenForm(initial={'gameid': gameid, 'color': color, 'bookenabled': enablebook}),
               'playForm': playForm(),
               'board': board,
               'depthForm': depthForm(initial={'depth': int(depth)}),
               'history': history,
               'modeForm': modeForm(initial={'mode': mode}),
               'enablebookForm': enablebookForm(initial={'enablebook': enablebook}),
               'addbookForm': addbookForm(),
               'bookmodeForm': bookmodeForm(initial={'bookmode': bookmode}),
               'saveForm': saveForm(),
               'loadForm': loadForm(),
               'hintForm': hintFormx,
    }

    return render(request, 'play.html', context)


def finished(request):
    return render(request, 'finished.html', {'winner': request.GET.get('winner')})


def killed(request):
    return render(request, 'killed.html')
