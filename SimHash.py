import hashlib


def generate_instances():
    for instance in input().strip().split(' '):
        yield instance


def generate_simhashes():
    N = int(input())
    if N > 1000:
        raise Exception('N must be less than 1000!')
    sh = []
    for _ in range(N):
        sh.append(simhash())
    return N, sh


def generate_queries():
    Q = int(input())
    if Q > 1000:
        raise Exception('Q must be less than 1000!')
    qs = []
    for _ in range(Q):
        qs.append(tuple([int(i) for i in input().strip().split(' ')]))
    return Q, qs


def simhash():
    length = 128
    sh = [0] * length
    for instance in generate_instances():
        md5_hash = hashlib.md5(instance.encode('utf-8')).hexdigest()
        binary_md5_hash = format(int(md5_hash, 16), f'0>{length}b')
        for i in range(length):
            if binary_md5_hash[i] == '1':
                sh[i] += 1
            else:
                sh[i] -= 1
    for i in range(length):
        if sh[i] >= 0:
            sh[i] = 1
        else:
            sh[i] = 0
    return ''.join([str(i) for i in sh])


def hamming_distance(simhash1, simhash2):
    return sum(sh1 != sh2 for sh1, sh2 in zip(simhash1, simhash2))


if __name__ == '__main__':
    N, simhashes = generate_simhashes()
    Q, queries = generate_queries()

    for I, K in queries:
        if I < 0 or I > N - 1 or K < 0 or K > 31:
            continue
        # we need to reduce the counter by 1 for the case when i == I
        counter = -1
        simhash_i = simhashes[I]
        for i in range(N):
            if hamming_distance(simhashes[i], simhash_i) <= K:
                counter += 1
        if counter < 0:
            counter = 0
        print(counter)
