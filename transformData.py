class transformData:
    def __init__(self, inputFile, outputFile):
        self.inputFile = inputFile
        self.outputFile = outputFile

    def transform(self):
        locations = set()
        data = dict()
        with open(self.inputFile) as f:
            for line in f:
                line = line.strip().split(',')
                date = f'{line[0]}/{line[1]}/{line[2]} {line[3]}'
                point = f'{line[7]}-{line[8]}/{line[10]}-{line[11]}'
                data[date] = dict()
                locations.add(point)
        for date in data:
            for location in locations:
                data[date].update({location: 0})
        with open(self.inputFile) as f:
            for line in f:
                line = line.strip().split(',')
                date = f'{line[0]}/{line[1]}/{line[2]} {line[3]}'
                point = f'{line[7]}-{line[8]}/{line[10]}-{line[11]}'
                data[date][point] = line[15]
        with open(self.outputFile, 'w') as f:
            locations = list(locations)
            f.write('time')
            for location in locations:
                f.write(f',{location}')
            f.write('\n')
            for date in data:
                f.write(f'{date}')
                for location in locations:
                    f.write(f',{data[date][location]}')
                f.write('\n')
            print('completed')


if __name__ == '__main__':
    obj = transformData('congestion.csv', 'output1.csv')
    obj.transform()