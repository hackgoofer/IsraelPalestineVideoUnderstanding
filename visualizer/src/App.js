import React from "react";
import { ResponsiveScatterPlot } from "@nivo/scatterplot";
import jsonData from "./search_index.json";

const formatDataForNivo = () => {
  let data = jsonData;
  const formatted_data = [];
  Object.keys(data).forEach((videoId) => {
    const video_data = data[videoId];

    if (
      !video_data ||
      !video_data["pro-palestinian"] ||
      !video_data["pro-palestinian"]["score"] ||
      !video_data["violence"] ||
      !video_data["violence"]["score"]
    ) {
      return;
    }

    formatted_data.push({
      id: videoId,
      data: [
        {
          x: video_data["pro-palestinian"]["score"],
          y: video_data["violence"]["score"],
        },
      ],
    });
  });

  return formatted_data;
};

function App() {
  console.log(formatDataForNivo());
  return (
    <div className="App" style={{ height: "500px" }}>
      <ResponsiveScatterPlot
        data={formatDataForNivo()}
        xScale={{ type: "linear", min: 0, max: 100 }}
        yScale={{ type: "linear", min: 0, max: 100 }}
        tooltip={({ node }) => <p>{"https://www.youtube.com/v=" + node.id}</p>}
        margin={{ top: 60, right: 40, bottom: 70, left: 90 }}
        axisTop={null}
        axisRight={null}
        axisBottom={{
          orient: "bottom",
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: "Pro-Palestinian Score",
          legendPosition: "middle",
          legendOffset: 46,
        }}
        axisLeft={{
          orient: "left",
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: "Violence Score",
          legendPosition: "middle",
          legendOffset: -60,
        }}
        legends={[
          {
            anchor: "bottom-right",
            direction: "column",
            justify: false,
            translateX: 130,
            translateY: 0,
            itemWidth: 130,
            itemHeight: 12,
            itemsSpacing: 5,
            itemDirection: "left-to-right",
            itemOpacity: 1,
            symbolSize: 12,
            effects: [
              {
                on: "hover",
                style: {
                  itemOpacity: 1,
                },
              },
            ],
          },
        ]}
      />
    </div>
  );
}

export default App;
