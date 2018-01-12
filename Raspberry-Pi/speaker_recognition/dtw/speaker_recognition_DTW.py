import sys
import librosa
import librosa.display

from numpy.linalg import norm
from subprocess import call
from matplotlib import pyplot as plt

from numpy import array, zeros, argmin, inf, equal, ndim

def dtw(x, y, dist):
    r, c = len(x), len(y)
    D0 = zeros((r + 1, c + 1))
    D0[0, 1:] = inf
    D0[1:, 0] = inf
    D1 = D0[1:, 1:] 
    for i in range(r):
        for j in range(c):
            D1[i, j] = dist(x[i], y[j])
    C = D1.copy()
    for i in range(r):
        for j in range(c):
            D1[i, j] += min(D0[i, j], D0[i, j+1], D0[i+1, j])
    if len(x)==1:
        path = zeros(len(y)), range(len(y))
    elif len(y) == 1:
        path = range(len(x)), zeros(len(x))
    else:
        path = _traceback(D0)
    return D1[-1, -1] / sum(D1.shape), C, D1, path

def _traceback(D):
    i, j = array(D.shape) - 2
    p, q = [i], [j]
    while ((i > 0) or (j > 0)):
        tb = argmin((D[i, j], D[i, j+1], D[i+1, j]))
        if (tb == 0):
            i -= 1
            j -= 1
        elif (tb == 1):
            i -= 1
        else: # (tb == 2):
            j -= 1
        p.insert(0, i)
        q.insert(0, j)
    return array(p), array(q)

if __name__ == '__main__':
	d_ip = sys.argv[1]
	t_ip = sys.argv[2]
	d_op = "".join((d_ip[0:-4], ".wav"))
	t_op = "".join((t_ip[0:-4], ".wav"))

	r=call('ffmpeg -i '+ d_ip +' -acodec pcm_s16le -ac 1 -ar 16000 '+ d_op, shell=True)
	r=call('ffmpeg -i '+ t_ip +' -acodec pcm_s16le -ac 1 -ar 16000 '+ t_op, shell=True)

	y1, sr1 = librosa.load(d_op)
	y2, sr2 = librosa.load(t_op)

	plt.subplot(2, 2, 1)
	mfcc1 = librosa.feature.mfcc(y1, sr1)
	librosa.display.specshow(mfcc1)

	plt.subplot(2, 2, 3)
	mfcc2 = librosa.feature.mfcc(y2, sr2)
	librosa.display.specshow(mfcc2)

	plt.subplot(1, 2, 2)
	dist, cost, acc_cost, path = dtw(mfcc1.T, mfcc2.T, dist=lambda x, y: norm(x - y, ord=1))
	print('Normalized distance between the two sounds:', dist)
	plt.imshow(cost.T, origin='lower', cmap=plt.cm.gray, interpolation='nearest')
	plt.plot(path[0], path[1], 'w')
	plt.xlim((-0.5, cost.shape[0]-0.5))
	plt.ylim((-0.5, cost.shape[1]-0.5))

	plt.show()
