option = {
    "xAxis": {
        "type": "category",
        "data": ["2017", "2018", "2019", "2020", "2021", "2022"],
    },
    "yAxis": {"type": "value"},
    "series": [{"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}],
}
st_echarts(
    options=option, height="400px",
)