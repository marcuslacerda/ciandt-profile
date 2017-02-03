FROM kibana:5.1.2
MAINTAINER mlacerda@ciandt.com

# install open or custom plugins
RUN kibana-plugin install https://github.com/marcuslacerda/kibana-oauth2-plugin/releases/download/0.2.1/oauth2-5.1.2.zip

# fix kibana 4.5 and sense plugin
# RUN chmod o+w /opt/kibana/optimize/.babelcache.json

#ENTRYPOINT ["/docker-entrypoint.sh"]
#CMD ["kibana"]
