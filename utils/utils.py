import pandas as pd

def createZigZagPoints(dfSeries, minSegSize=0.1, sizeInDevs=0.5):
    minRetrace = minSegSize

    curVal = dfSeries[0]
    curPos = dfSeries.index[0]
    curDir = 1
    dfRes = pd.DataFrame(index=dfSeries.index, columns=["Dir", "Value"])
    for ln in dfSeries.index:
        if ((dfSeries[ln] - curVal) * curDir >= 0):
            curVal = dfSeries[ln]
            curPos = ln
        else:
            retracePrc = abs((dfSeries[ln] - curVal) / curVal * 100)
            if (retracePrc >= minRetrace):
                dfRes.loc[curPos, 'Value'] = curVal
                dfRes.loc[curPos, 'Dir'] = curDir
                curVal = dfSeries[ln]
                curPos = ln
                curDir = -1 * curDir
    dfRes[['Value']] = dfRes[['Value']].astype(float)
    return (dfRes)