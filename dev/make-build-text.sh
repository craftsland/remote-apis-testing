#!/bin/bash
usage(){
  echo Usage: update-metrics-page.sh RE_NAME
}


if [ $# -lt 1 ]; then
  echo "Expecting RE_NAME"
  usage
  exit 1
fi

case $1 in
  buildbarn)
    SERVERS="buildbarn buildbarn-concurrency-1 buildbarn-incremental buildbarn-concurrency-1-incremental"
    METRICSPAGE="buildbarn-metrics.md"
    ;;
  buildfarm)
    SERVERS="buildfarm buildfarm-concurrency-1 buildfarm-incremental buildfarm-concurrency-1-incremental"
    METRICSPAGE="buildfarm-metrics.md"
    ;;
  buildgrid)
    SERVERS="buildgrid buildgrid-incremental"
    METRICSPAGE="buildgrid-metrics.md"
    ;;
  *)
    echo "Unknown RE_NAME supplied"
    exit 1
    ;;
esac
for server in $SERVERS; do
        BADGE="![]($WIKI_URL/badges/$(tr - _ <<< $server)-time.svg)"
        CPU_PDF="CPU [PDF]($WIKI_URL/metrics/$server-cpu.pdf)"
        IO_PDF="IO [PDF]($WIKI_URL/metrics/$server-net-disk.pdf)"
        if [ -f $CI_PIPELINE_ID/metrics/$server-cpu.txt ]; then
          CPU_DASH_URL=`cat $CI_PIPELINE_ID/metrics/$server-cpu.txt`
        fi
        if [ -f $CI_PIPELINE_ID/metrics/$server-net-disk.txt ]; then
          IO_DASH_URL=`cat $CI_PIPELINE_ID/metrics/$server-net-disk.txt`
        fi
        if [ ! -z $CPU_DASH_URL ]; then
          CPU_DASH="[Dash]($CPU_DASH_URL)"
        else
          CPU_DASH="N/A"
        fi
        if [ ! -z $IO_DASH_URL ]; then
          IO_DASH="[Dash]($IO_DASH_URL)"
        else
          IO_DASH="N/A"
        fi
        BUILD_TEXT="$BUILD_TEXT$BADGE$BR$CPU_PDF $CPU_DASH$BR$IO_PDF $IO_DASH$PIPE_SYM"
done

sed -i "/-|$/a$PIPE_SYM$DATE_SYM$BR$PIPELINE_SYM$PIPE_SYM$BUILD_TEXT" $METRICSPAGE
