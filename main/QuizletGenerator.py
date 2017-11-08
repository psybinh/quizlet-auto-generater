from dictionary_dot_com import DictionaryReference

if __name__ == "__main__":
     input = open("input.txt")
     output = open("output.txt", "w")
     for line in input:
          word = line.rstrip()
          def_word = DictionaryReference(word)
          def_word.get_definitions()
          output.write(def_word.__str__() + "\t" + def_word.get_top3() + "\n\n")
     input.close()
     output.close()