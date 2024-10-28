import Wordcloud from "@visx/wordcloud/lib/Wordcloud";
import { Text } from "@visx/text";
import { scaleLog } from "@visx/scale";
import { useEffect, useState } from "react";
import Select from "react-select";
import "./App.css";

interface WordData {
  text: string;
  value: number;
}

interface GenreData {
  [key: string]: WordData[];
}

function App() {
  const [genres, setGenres] = useState<{ value: string; label: string }[]>([]);
  const [selectedGenre, setSelectedGenre] = useState<{
    value: string;
    label: string;
  } | null>(null);
  const [words, setWords] = useState<GenreData>({});
  const [wordCloudType, setWordCloudType] = useState<"tfidf" | "common">(
    "tfidf"
  );

  useEffect(() => {
    const json =
      wordCloudType === "tfidf"
        ? "tfidf_words_by_genre.json"
        : "most_common_words_by_genre.json";

    fetch(json)
      .then((response) => response.json())
      .then((data: GenreData) => {
        setGenres(
          Object.keys(data).map((genre) => ({ value: genre, label: genre }))
        );
        setWords(data);
      });
  }, [wordCloudType]);

  const handleGenreChange = (
    selectedOption: { value: string; label: string } | null
  ) => {
    setSelectedGenre(selectedOption);
  };

  const wordcloudData = selectedGenre ? words[selectedGenre.value] : [];

  const colors = ["#ffb3ba", "#ffdfba", "#C3B1E1", "#baffc9", "#bae1ff"];

  function getRotationDegree() {
    const rand = Math.random();
    const degree = rand > 0.5 ? 60 : -60;
    return rand * degree;
  }

  const fixedValueGenerator = () => 0.5;

  const fontScale = scaleLog({
    domain: [
      Math.min(...wordcloudData.map((w) => w.value)),
      Math.max(...wordcloudData.map((w) => w.value)),
    ],
    range: [10, 100],
  });
  const fontSizeSetter = (datum: WordData) => fontScale(datum.value);

  return (
    <div className="container">
      <h1>HitHelper</h1>
      <hr className="divider" />
      <span>
        Do you want to see wordclouds based on TF-IDF values or common words?
      </span>
      <div className="radio-buttons">
        <label>
          <input
            type="radio"
            value="tfidf"
            checked={wordCloudType === "tfidf"}
            onChange={() => setWordCloudType("tfidf")}
          />
          TF-IDF values
        </label>
        <label>
          <input
            type="radio"
            value="common"
            checked={wordCloudType === "common"}
            onChange={() => setWordCloudType("common")}
          />
          Common words
        </label>
      </div>
      <span>Select your genre of choice!</span>
      <Select
        options={genres}
        onChange={handleGenreChange}
        placeholder="Select a genre"
        className="select"
      />
      <Wordcloud
        words={wordcloudData}
        width={1000}
        height={500}
        fontSize={fontSizeSetter}
        font={"Impact"}
        padding={2}
        spiral={"archimedean"}
        rotate={getRotationDegree}
        random={fixedValueGenerator}
      >
        {(cloudWords) =>
          cloudWords.map((w, i) => (
            <Text
              key={w.text}
              fill={colors[i % colors.length]}
              textAnchor={"middle"}
              transform={`translate(${w.x}, ${w.y}) rotate(${w.rotate})`}
              fontSize={w.size}
              fontFamily={w.font}
            >
              {w.text}
            </Text>
          ))
        }
      </Wordcloud>
    </div>
  );
}

export default App;
