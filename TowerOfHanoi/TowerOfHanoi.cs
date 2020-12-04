using System.Collections.Generic;

namespace Hanoi
{
    public static class TowerOfHanoi
    {

        public static int GetNumberOfSteps(int numDiscs)
        {
            if (numDiscs == 0)
            {
                return 0;
            }
            if (numDiscs < 0)
            {
                return -1;
            }
            if (numDiscs == 1)
            {
                return 1;
            }
            return GetNumberOfSteps(numDiscs - 1) + GetNumberOfSteps(1) + GetNumberOfSteps(numDiscs - 1);
        }

        public static List<List<int>[]> SolveTowerOfHanoi(int numDiscs)
        {
            if (numDiscs < 1)
            {
                List<List<int>[]> emptyhanoiTower = new List<List<int>[]>(0);
                return emptyhanoiTower;
            }
            int steps = GetNumberOfSteps(numDiscs);

            List<List<int>[]> hanoiTower = new List<List<int>[]>(steps);

            List<int>[] hanoiPlate = new List<int>[3];
            List<int> startTower = new List<int>(numDiscs);
            List<int> tempTower = new List<int>(numDiscs);
            List<int> endTower = new List<int>(numDiscs);

            List<int> next = new List<int>(steps * 2); // 순서들 적을 리스트

            Hanoisteps(numDiscs, 1, 2, 3, next);  //리스트에 순서들 적어왔음

            for (int i = numDiscs; i > 0; i--)
            {
                startTower.Add(i);
            }

            hanoiPlate[0] = startTower;
            hanoiPlate[1] = tempTower;
            hanoiPlate[2] = endTower;

            hanoiTower.Add(hanoiPlate);  //하노이탑 첫스타트

            for (int i = 0; i < steps; i++)
            {
                List<int>[] tempHanoiPlate = new List<int>[3];
                List<int> tempStartTower = new List<int>(numDiscs);
                List<int> tempTempTower = new List<int>(numDiscs);
                List<int> tempEndTower = new List<int>(numDiscs);
                if (i == 0)
                {
                    for (int j = numDiscs; j > 0; j--)
                    {
                        tempStartTower.Add(j);
                    }
                    tempHanoiPlate[0] = tempStartTower;
                    tempHanoiPlate[1] = tempTempTower;
                    tempHanoiPlate[2] = tempEndTower;
                }
                if (i > 0)
                {
                    if (hanoiTower[i][0].Count > 0)
                    {
                        for (int j = 0; j < hanoiTower[i][0].Count; j++)
                        {
                            int discValue = hanoiTower[i][0][j];
                            tempStartTower.Add(discValue);
                        }
                    }
                    if (hanoiTower[i][1].Count > 0)
                    {
                        for (int j = 0; j < hanoiTower[i][1].Count; j++)
                        {
                            int discValue = hanoiTower[i][1][j];
                            tempTempTower.Add(discValue);
                        }
                    }
                    if (hanoiTower[i][2].Count > 0)
                    {
                        for (int j = 0; j < hanoiTower[i][2].Count; j++)
                        {
                            int discValue = hanoiTower[i][2][j];
                            tempEndTower.Add(discValue);
                        }
                    }
                }
                if (next[2 * i] == 1)
                {
                    if (next[2 * i + 1] == 2)
                    {
                        tempTempTower.Add(tempStartTower[(tempStartTower.Count) - 1]);
                        tempStartTower.Remove(tempStartTower[(tempStartTower.Count) - 1]);
                    }
                    else
                    {
                        tempEndTower.Add(tempStartTower[(tempStartTower.Count) - 1]);
                        tempStartTower.Remove(tempStartTower[(tempStartTower.Count) - 1]);
                    }
                }
                if (next[2 * i] == 2)
                {
                    if (next[2 * i + 1] == 1)
                    {
                        tempStartTower.Add(tempTempTower[(tempTempTower.Count) - 1]);
                        tempTempTower.Remove(tempTempTower[(tempTempTower.Count) - 1]);
                    }
                    else
                    {
                        tempEndTower.Add(tempTempTower[(tempTempTower.Count) - 1]);
                        tempTempTower.Remove(tempTempTower[(tempTempTower.Count) - 1]);
                    }
                }
                if (next[2 * i] == 3)
                {
                    if (next[2 * i + 1] == 1)
                    {
                        tempStartTower.Add(tempEndTower[(tempEndTower.Count) - 1]);
                        tempEndTower.Remove(tempEndTower[(tempEndTower.Count) - 1]);
                    }
                    else
                    {
                        tempTempTower.Add(tempEndTower[(tempEndTower.Count) - 1]);
                        tempEndTower.Remove(tempEndTower[(tempEndTower.Count) - 1]);
                    }
                }
                tempHanoiPlate[0] = tempStartTower;
                tempHanoiPlate[1] = tempTempTower;
                tempHanoiPlate[2] = tempEndTower;

                hanoiTower.Add(tempHanoiPlate);
            }
            return hanoiTower;
        }
        public static void Hanoisteps(int discs, int from, int temp, int to, List<int> array)
        {
            if (discs > 0)
            {
                Hanoisteps(discs - 1, from, to, temp, array);
                array.Add(from);
                array.Add(to);
                Hanoisteps(discs - 1, temp, from, to, array);
            }
        }
    }
}
