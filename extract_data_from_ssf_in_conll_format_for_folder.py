# how to run the code
# python3 extract_data_from_ssf_in_conll_format_for_folder.py --input InputFolderPath --output OutputFolderPath --level level
# no need to create a output folder, only give a name
# author : Pruthwik Mishra, LTRC, IIIT-H
import ssfAPI as ssf
import os
import argparse
import re


def readFilesAndExtractSentencesInConLL(inputFolderPath, outputFolderPath, level=0):
    fileList = ssf.folderWalk(inputFolderPath)
    newFileList = []
    for fileName in fileList:
        xFileName = fileName.split('/')[-1]
        if xFileName == 'err.txt' or xFileName.split('.')[-1] in ['comments', 'bak'] or xFileName[:4] == 'task':
            continue
        else:
            newFileList.append(fileName)
    newFileList = sorted(newFileList)
    for fileName in newFileList:
        print(fileName)
        d = ssf.Document(fileName)
        sentencesList = []
        for tree in d.nodeList:
            if level == 0:
                sentencesList.append('\n'.join([token for token in tree.generateSentence().split() if not re.search('^NUL', token)]) + '\n')
            elif level == 1:
                tokensWithPOS = []
                for chunkNode in tree.nodeList:
                    if chunkNode.__class__.__name__ == 'ChunkNode':
                        if re.search('^NULL', chunkNode.type):
                            continue
                        for node in chunkNode.nodeList:
                            if node.__class__.__name__ == 'ChunkNode':
                                continue
                            if not re.search('^NUL', node.lex):
                                if re.search('UNK', node.type):
                                    break
                                if not node.type:
                                    node.type = 'N_NNP'
                                tokensWithPOS.append(node.lex + '\t' + node.type.replace('__', '_'))
                    elif chunkNode.__class__.__name__ == 'Node':
                        if not re.search('^NUL', chunkNode.lex):
                            tokensWithPOS.append(chunkNode.lex + '\t' + chunkNode.type.replace('__', '_'))
                sentencesList.append('\n'.join(tokensWithPOS) + '\n')
            elif level == 2:
                tokensWithPOSMorph = []
                for chunkNode in tree.nodeList:
                    if re.search('^NULL', chunkNode.type):
                        continue
                    for node in chunkNode.nodeList:
                        if not re.search('^NUL', node.lex):
                            # the below code ignores sentences with UNK pos tag.
                            if re.search('UNK', node.type):
                                break
                            pos = node.type.replace('__', '_')
                            if node.getAttribute('af'):
                                tokensWithPOSMorph.append(node.lex + '\t' + pos + '\t' + node.getAttribute('af'))
                            else:
                                tokensWithPOSMorph.append(node.lex + '\t' + pos + '\t' + node.lex + ',,,,,,,')
                sentencesList.append('\n'.join(tokensWithPOSMorph) + '\n')
            elif level == 3:
                tokenPOSAndChunk = []
                for chunkNode in tree.nodeList:
                    if re.search('^NULL', chunkNode.type):
                        continue
                    for indexNode, node in enumerate(chunkNode.nodeList):
                        if re.search('UNK', node.type):
                            break
                        if indexNode == 0:
                            if not re.search('^NUL', node.lex):
                                tokenPOSAndChunk.append(node.lex + '\t' + node.type.replace('__', '_') + '\tB-' + chunkNode.type)
                        else:
                            if not re.search('^NUL', node.lex):
                                lastChunk = tokenPOSAndChunk[-1].split('\t')[2]
                                lastChunkType = lastChunk.split('-')[1]
                                if lastChunkType == chunkNode.type:
                                    tokenPOSAndChunk.append(node.lex + '\t' + node.type.replace('__', '_') + '\tI-' + chunkNode.type)
                                else:
                                    tokenPOSAndChunk.append(node.lex + '\t' + node.type.replace('__', '_') + '\tB-' + chunkNode.type)
                sentencesList.append('\n'.join(tokenPOSAndChunk) + '\n')
            else:
                tokenPOSChunkMorph = []
                for chunkNode in tree.nodeList:
                    if re.search('^NULL', chunkNode.type):
                        continue
                    for indexNode, node in enumerate(chunkNode.nodeList):
                        if re.search('UNK', node.type):
                            break
                        if node.getAttribute('af'):
                            morphFeat = node.getAttribute('af')
                        else:
                            morphFeat = node.lex + ',,,,,,,'
                        if indexNode == 0:
                            if not re.search('^NUL', node.lex):
                                tokenPOSChunkMorph.append(node.lex + '\t' + node.type.replace('__', '_') + '\tB-' + chunkNode.type + '\t' + morphFeat)
                        else:
                            if not re.search('^NUL', node.lex):
                                lastChunk = tokenPOSChunkMorph[-1].split('\t')[2]
                                lastChunkType = lastChunk.split('-')[1]
                                if lastChunkType == chunkNode.type:
                                    tokenPOSChunkMorph.append(node.lex + '\t' + node.type.replace('__', '_') + '\tI-' + chunkNode.type + '\t' + morphFeat)
                                else:
                                    tokenPOSChunkMorph.append(node.lex + '\t' + node.type.replace('__', '_') + '\tB-' + chunkNode.type + '\t' + morphFeat)
                sentencesList.append('\n'.join(tokenPOSChunkMorph) + '\n')
            outFilePath = os.path.join(outputFolderPath, fileName[fileName.rfind('/') + 1:])
            writeListToFile(sentencesList, outFilePath)


def writeListToFile(dataList, outFilePath):
    with open(outFilePath, 'w', encoding='utf-8') as fileWrite:
        fileWrite.write('\n'.join(dataList) + '\n')
        fileWrite.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='inp', help="Add the input folder path")
    parser.add_argument('--output', dest='out', help="Add the output folder path")
    parser.add_argument('--level', dest='level', help="Add the level 0: token, 1: token + pos, 2: token + pos + morph, 3 for token + pos + chunk, 4 for token + pos + chunk + morph", type=int, default=0)
    args = parser.parse_args()
    if not os.path.isdir(args.out):
        os.mkdir(args.out)
    readFilesAndExtractSentencesInConLL(args.inp, args.out, args.level)

if __name__ == '__main__':
    main()
