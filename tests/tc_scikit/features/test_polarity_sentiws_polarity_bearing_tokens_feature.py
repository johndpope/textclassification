import unittest

import frameworks.tc_scikit.features.sentiws_polarity_bearing_tokens_feature as sentiws_polarity_bearing_tokens_feature
from experiments.argument_mining.models.classical_ml.thf_sentence_export import THFSentenceExport
from frameworks.tc_scikit.models.token import Token


class THFSentenceSentiWSPolarityBearingTokens(unittest.TestCase):
    def test_count_polarity_bearing_tokens_example1(self):
        tokens = []
        tokens.append(Token(token_index_in_sentence=1, text=None, polarity_sentiws=0.5))
        tokens.append(Token(token_index_in_sentence=2, text=None))
        tokens.append(Token(token_index_in_sentence=3, text=None, polarity_sentiws=1.5))
        thf_sentence = THFSentenceExport(None, None, None, tokens, None, 1)
        feature_value = sentiws_polarity_bearing_tokens_feature.count_polarity_bearing_tokens(thf_sentence)
        expected_value = [2]
        self.assertEqual(feature_value, expected_value)

    def test_count_polarity_bearing_tokens_example2(self):
        tokens = []
        tokens.append(Token(token_index_in_sentence=1, text=None))
        tokens.append(Token(token_index_in_sentence=2, text=None))
        tokens.append(Token(token_index_in_sentence=3, text=None))
        thf_sentence = THFSentenceExport(None, None, None, tokens, None, 1)
        feature_value = sentiws_polarity_bearing_tokens_feature.count_polarity_bearing_tokens(thf_sentence)
        expected_value = [0]
        self.assertEqual(feature_value, expected_value)

    def test_count_polarity_bearing_tokens_example3(self):
        tokens = []
        tokens.append(Token(token_index_in_sentence=1, text=None))
        tokens.append(Token(token_index_in_sentence=2, text=None, polarity_sentiws=-1))
        tokens.append(Token(token_index_in_sentence=3, text=None, polarity_sentiws=-1.5))
        thf_sentence = THFSentenceExport(None, None, None, tokens, None, 1)
        feature_value = sentiws_polarity_bearing_tokens_feature.count_polarity_bearing_tokens(thf_sentence)
        expected_value = [2]
        self.assertEqual(feature_value, expected_value)


if __name__ == '__main__':
    unittest.main()
