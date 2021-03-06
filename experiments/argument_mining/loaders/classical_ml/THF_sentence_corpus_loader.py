#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import logging

from experiments.argument_mining.models.classical_ml.thf_sentence_export import THFSentenceExport
from frameworks.tc_scikit.models.dependency import Dependency
from frameworks.tc_scikit.models.token import Token

logger = logging.getLogger()


def load_dataset(file_path, data_version='v2', group_claims=True):
    if data_version == 'v3':
        dataset = load_v3(file_path=file_path, group_claims=group_claims)
    else:
        dataset = load(file_path=file_path, group_claims=group_claims)
    X = dataset
    y = [item.label for item in dataset]
    return X, y


def load_v3(file_path='data/THF/sentence/subtaskA_train.json', group_claims=True):
    logger.debug(u'Parsing JSON File: {}'.format(file_path))
    sentences = []
    with open(file_path, encoding='utf-8') as data_file:
        data = json.load(data_file)
        for sentence in data:
            sentence_tokens = sentence["NLP"]["tokens"]
            tokens = []
            for token in sentence_tokens:
                token.pop("embedding")
                token.pop("mate_tools_pos_tag")  # remove legacy token information, replaced by spaCy
                token.pop("mate_tools_lemma")  # remove legacy token information, replaced by spaCy
                token.pop("pos_tag")  # remove legacy token information, replaced by spaCy
                token.pop("tree_tagger_lemma")  # remove legacy token information, replaced by spaCy
                token_model = Token(**token)
                tokens.append(token_model)
            dependencies = []
            dependency_tokens = sentence["NLP"]["dependencies"]
            for dependency in dependency_tokens:
                dependency_model = Dependency(**dependency)
                dependencies.append(dependency_model)
            label = sentence["Label"]
            if group_claims:
                if label == 'ClaimContra' or label == 'ClaimPro':
                    label = 'Claim'
            sentence_model = THFSentenceExport(sentence["UniqueID"], label, sentence["Text"], tokens,
                                               dependencies, textdepth=sentence["TextDepth"])
            sentences.append(sentence_model)
    logger.info('Parsed {} sentences'.format(len(sentences)))
    return sentences


def load(file_path='data/THF/sentence/subtaskA_train.json', group_claims=True):
    """
    Loads the THF corpus from an JSON file
    :param file_path: relative path to the JSON file
    :return:
    """
    logger.debug(u'Parsing JSON File: {}'.format(file_path))
    sentences = []
    with open(file_path, encoding='utf-8') as data_file:
        data = json.load(data_file)
        for sentence in data:
            sentence_tokens = sentence["NLP"]["Sentences"][0]["Tokens"]
            tokens = []
            dependencies = []
            for token in sentence_tokens:
                token_model = Token(token["TokenIndexInSentence"],
                                    token["Text"],
                                    pos_tag=token["POSTag"],
                                    iwnlp_lemma=parse_IWNLP_lemma(token.get("IWNLPLemma", None)),
                                    polarity=parse_polarity((token.get("Polarity", None))))
                tokens.append(token_model)
            dependency_tokens = sentence["NLP"]["Sentences"][0]["Dependencies"]
            for dependency in dependency_tokens:
                dependency_model = Dependency(dependency["TokenID"], dependency["DependencyRelation"],
                                              dependency["DependencyHeadTokenID"])
                dependencies.append(dependency_model)
            label = sentence["Label"]
            if group_claims:
                if label == 'ClaimContra' or label == 'ClaimPro':
                    label = 'Claim'
            sentence_model = THFSentenceExport(sentence["UniqueID"], label, sentence["Text"], tokens,
                                               dependencies)
            sentences.append(sentence_model)
    logger.info('Parsed {} sentences'.format(len(sentences)))
    return sentences


def parse_IWNLP_lemma(text):
    if not text:
        return None
    else:
        return text


def parse_tree_tagger_lemma(text):
    if not text:
        return None
    else:
        return text


def parse_polarity(polarity):
    return polarity
