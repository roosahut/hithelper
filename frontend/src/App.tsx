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

  useEffect(() => {
    fetch("/most_common_words_per_genre.json")
      .then((response) => response.json())
      .then((data: GenreData) => {
        setGenres(
          Object.keys(data).map((genre) => ({ value: genre, label: genre }))
        );
        setWords(data);
      });
  }, []);

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
      <Select
        options={genres}
        onChange={handleGenreChange}
        placeholder="Select a genre"
      />
      <Wordcloud
        words={wordcloudData}
        width={800}
        height={800}
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
