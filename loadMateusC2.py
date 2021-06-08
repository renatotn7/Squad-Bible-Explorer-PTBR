import transformers
from transformers import pipeline

# source: https://pt.wikipedia.org/wiki/Pandemia_de_COVID-19
context = r"""Jesus Cristo, Filho de Davi, Filho de Abraão
O nascimento de Jesus Cristo ocorreu da seguinte maneira: Estando Maria, sua mãe, prometida em casamento a José, antes que coabitassem, achou-se grávida pelo Espírito Santo. Então, José, seu esposo, sendo um homem justo e não querendo expô-la à desonra pública, planejou deixá-la sem que ninguém soubesse a razão. Mas, enquanto meditava sobre isso, eis que, em sonho, lhe apareceu um anjo do SENHOR, dizendo: "José, filho de Davi, não temas receber a Maria como sua mulher, pois o que nela está gerado é do Espírito Santo. Ela dará à luz um filho, e lhe porás o nome de Jesus, porque Ele salvará o seu povo dos seus pecados”. Tudo isso aconteceu para que se cumprisse o que o SENHOR havia dito através do profeta: "Eis que a virgem conceberá e dará à luz um filho, e Ele será chamado de Emanuel”, que significa "Deus conosco”. José, ao despertar do sonho, fez o que o Anjo do SENHOR lhe tinha ordenado e recebeu Maria como sua mulher. Contudo, não coabitou com ela enquanto ela não deu à luz o filho primogênito. E José lhe colocou o nome de Jesus.
Após o nascimento de Jesusem Belém da Judéia, nos dias do rei Herodes, eis que alguns sábios vindos do Oriente chegaram a Jerusalém. E, indagavam: Onde está aquele que é nascido rei dos judeus? Pois do Oriente vimos a sua estrela e viemos adorá-lo. Quando o rei Herodes ouviu isso, ficou perturbado e toda a Jerusalém com ele. Tendo reunido todos os príncipes dos sacerdotes e os escribas do povo, perguntou-lhes onde havia de nascer o Cristo. E eles lhe responderam: Em Belém da Judéia, pois assim escreveu o profeta:
Mas tu, Belém, da terra de Judá, de modo algum és a menor entre as principais cidades de Judá; pois de ti sairá o Guia, que como pastor, conduzirá Israel, o meu povo.
Então Herodes, chamando secretamente os sábios, interrogou-os exatamente acerca do tempo em que a estrela lhes aparecera. Mandou-os a Belém e disse: Ide, e perguntai diligentemente pelo menino, e quando o achardes, comunicai-me, para que também eu vá e o adore. Após terem ouvido o rei, seguiram o seu caminho, e a estrela que tinham visto no Oriente foi adiante deles, até que finalmente parou sobre o lugar onde estava o menino. E vendo eles a estrela, alegraram-se com grande e intenso júbilo. Ao entrarem na casa, encontraram o menino com Maria, sua mãe, e prostrando-se o adoraram. Então abriram seus tesouros e lhe ofertaram presentes: ouro, incenso e mirra. E, sendo por divina revelação avisados em sonhos para que não voltassem para junto de Herodes, retornaram para a sua terra, por outro caminho. A fuga para o Egito
Depois que partiram, eis que um anjo do SENHOR apareceu a José em sonho e lhe disse: Levanta-te, toma o menino e sua mãe, e foge para o Egito. Permanece lá até que eu te diga, pois Herodes há de procurar o menino para o matar.
José se levantou, tomou o menino e sua mãe, durante a noite, e partiu para o Egito. E esteve lá até a morte de Herodes. E assim se cumpriu o que o SENHOR tinha dito através do profeta: Do Egito chamei o meu filho.
Quando Herodes percebeu que havia sido iludido pelos sábios, irou-se terrivelmente e mandou matar todos os meninos de dois anos para baixo, em Belém e em todas as circunvizinhanças, de acordo com as informações que havia obtido dos sábios. Então se cumpriu o que fora dito pelo profeta Jeremias:
Ouviu-se uma voz em Ramá, pranto e grande lamentação; é Raquel que chora por seus filhos e recusa ser consolada, pois já não existem. O retorno para Israel
Após a morte de Herodes, eis que um anjo do SENHOR apareceu em sonho a José, no Egito, e disse-lhe: Dispõe-te, toma o menino e sua mãe, e vai para a terra de Israel; porque já estão mortos os que procuravam tirar a vida do menino. Então, José se levantou, tomou o menino e sua mãe, e foi para a terra de Israel. Mas, ao ouvir que Arquelau estava reinando na Judéia, em lugar de seu pai Herodes, teve medo de ir para lá. Contudo, tendo sido avisado em sonho por divina revelação, seguiu para as regiões da Galiléia. Ao chegar, foi viver numa cidade chamada Nazaré. Cumpriu-se assim o que fora dito pelos profetas: Ele será chamado Nazareno.
Naqueles dias surgiu João Batista pregando no deserto da Judéia; e dizia: Arrependei-vos, porque o Reino dos céus está próximo.
Este é aquele que foi anunciado pelo profeta Isaías: Voz do que clama no deserto: Preparai o caminho do SENHOR, endireitai as suas veredas.
João tinha suas roupas feitas de pêlos de camelo e usava um cinto de couro na cintura. Alimentava-se com gafanhotos e mel silvestre. A ele vinha gente de Jerusalém, de toda a Judéia e de toda a província adjacente ao Jordão. Confessando os seus pecados, eram batizados por João no rio Jordão.
E, vendo ele muitos dos fariseus e dos saduceus que vinham ao seu batismo, dizia-lhes: Raça de víboras, quem vos ensinou a fugir da ira futura? Produzi, sim, frutos que mostrem vosso arrependimento! Não presumais de vós mesmos, dizendo: Temos por pai a Abraão; porque eu vos digo que mesmo destas pedras Deus pode gerar filhos a Abraão. O machado já está posto à raiz das árvores, e toda árvore, pois, que não produz bom fruto é cortada e lançada no fogo.
Eu, em verdade, vos batizo com água, para arrependimento; mas depois de mim vem alguém mais poderoso do que eu, tanto que não sou digno nem de levar as suas sandálias. Ele vos batizará com o Espírito Santo e com fogo. Ele traz a pá em sua mão e separará o trigo da palha.Recolherá no celeiro o seu trigo e queimará a palha no fogo que jamais se apaga. O batismo de Jesus
Então Jesus veio da Galiléia ao Jordão para ser batizado por João. Mas João se recusava, justificando: Sou eu quem precisa ser batizado por ti, e vens tu a mim? Jesus, entretanto, declarou: Deixe assim, por enquanto; pois assim convém que façamos, para cumprir toda a justiça. E João concordou. E, sendo Jesus batizado, saiu logo da água, e eis que se abriram os céus, e viu o Espírito de Deus descendo como pomba e vindo sobre Ele. Em seguida, uma voz dos céus disse: Este é meu Filho amado, em quem muito me agrado.
Após o nascimento de Jesusem Belém da Judéia, nos dias do rei Herodes, eis que alguns sábios vindos do Oriente chegaram a Jerusalém. E, indagavam: Onde está aquele que é nascido rei dos judeus? Pois do Oriente vimos a sua estrela e viemos adorá-lo. Quando o rei Herodes ouviu isso, ficou perturbado e toda a Jerusalém com ele. Tendo reunido todos os príncipes dos sacerdotes e os escribas do povo, perguntou-lhes onde havia de nascer o Cristo. E eles lhe responderam: Em Belém da Judéia, pois assim escreveu o profeta:
Mas tu, Belém, da terra de Judá, de modo algum és a menor entre as principais cidades de Judá; pois de ti sairá o Guia, que como pastor, conduzirá Israel, o meu povo.
Então Herodes, chamando secretamente os sábios, interrogou-os exatamente acerca do tempo em que a estrela lhes aparecera. Mandou-os a Belém e disse: Ide, e perguntai diligentemente pelo menino, e quando o achardes, comunicai-me, para que também eu vá e o adore. Após terem ouvido o rei, seguiram o seu caminho, e a estrela que tinham visto no Oriente foi adiante deles, até que finalmente parou sobre o lugar onde estava o menino. E vendo eles a estrela, alegraram-se com grande e intenso júbilo. Ao entrarem na casa, encontraram o menino com Maria, sua mãe, e prostrando-se o adoraram. Então abriram seus tesouros e lhe ofertaram presentes: ouro, incenso e mirra. E, sendo por divina revelação avisados em sonhos para que não voltassem para junto de Herodes, retornaram para a sua terra, por outro caminho. A fuga para o Egito
Depois que partiram, eis que um anjo do SENHOR apareceu a José em sonho e lhe disse: Levanta-te, toma o menino e sua mãe, e foge para o Egito. Permanece lá até que eu te diga, pois Herodes há de procurar o menino para o matar.
José se levantou, tomou o menino e sua mãe, durante a noite, e partiu para o Egito. E esteve lá até a morte de Herodes. E assim se cumpriu o que o SENHOR tinha dito através do profeta: Do Egito chamei o meu filho.
Quando Herodes percebeu que havia sido iludido pelos sábios, irou-se terrivelmente e mandou matar todos os meninos de dois anos para baixo, em Belém e em todas as circunvizinhanças, de acordo com as informações que havia obtido dos sábios. Então se cumpriu o que fora dito pelo profeta Jeremias:
Ouviu-se uma voz em Ramá, pranto e grande lamentação; é Raquel que chora por seus filhos e recusa ser consolada, pois já não existem. O retorno para Israel
Após a morte de Herodes, eis que um anjo do SENHOR apareceu em sonho a José, no Egito, e disse-lhe: Dispõe-te, toma o menino e sua mãe, e vai para a terra de Israel; porque já estão mortos os que procuravam tirar a vida do menino. Então, José se levantou, tomou o menino e sua mãe, e foi para a terra de Israel. Mas, ao ouvir que Arquelau estava reinando na Judéia, em lugar de seu pai Herodes, teve medo de ir para lá. Contudo, tendo sido avisado em sonho por divina revelação, seguiu para as regiões da Galiléia. Ao chegar, foi viver numa cidade chamada Nazaré. Cumpriu-se assim o que fora dito pelos profetas: Ele será chamado Nazareno.
Jesus, vendo as multidões, subiu a um monte e, assentando-se, os seus discípulos aproximaram-se dele. E Jesus, abrindo a boca, os ensinava, dizendo:
Bem-aventurados os pobres em espírito, pois deles é o Reino dos Céus.
Bem-aventurados os que choram, porque serão consolados.
Bem-aventurados os humildes, porque herdarão a terra.
Bem-aventurados os que têm fome e sede de justiça, porque serão fartos.
Bem-aventurados os misericordiosos, porque alcançarão misericórdia.
Bem-aventurados os limpos de coração, porque verão a Deus.
Bem-aventurados os pacificadores, porque serão chamados filhos de Deus.
Bem-aventurados os que sofrem perseguição por causa da justiça, porque deles é o Reino dos Céus.
Bem-aventurados sois vós quando vos insultarem, e perseguirem e, mentindo, disserem todo o mal contra vós, por minha causa. Exultai e alegrai-vos sobremaneira, pois é esplêndida a vossa recompensa nos céus; porque assim perseguiram os profetas que viveram antes de vós. O cristão deve ser sal e luz
Vós sois o sal da terra. Mas se o sal perder o seu sabor, com o que se há de temperar? Para nada mais presta, senão para se lançar fora e ser pisado pelos homens.
Vós sois a luz do mundo. Uma cidade edificada sobre um monte não pode ser escondida. Igualmente não se acende uma candeia para colocá-la debaixo de um cesto. Ao contrário, coloca-se no velador e, assim, ilumina a todos os que estão na casa. Assim deixai a vossa luz resplandecer diante dos homens, para que vejam as vossas boas obras e glorifiquem o vosso Pai que está nos céus. A Lei se cumpre em Cristo
Não penseis que vim destruir a Lei ou os Profetas. Eu não vim para anular, mas para cumprir. Com toda a certeza vos afirmo que, até que os céus e a terra passem, nem um iou o mínimo traço se omitirá da Lei até que tudo se cumpra. Qualquer, pois, que violar um destes menores mandamentos e assim ensinar aos homens será chamado o menor no Reino dos Céus; aquele, porém, que os cumprir e ensinar será chamado grande no Reino dos Céus.
Porque vos digo que, se a vossa justiça não exceder a dos escribas e fariseus, de modo nenhum entrareis no Reino dos Céus.
Ouvistes que foi dito aos antigos: Não matarás; mas quem assassinar estará sujeito a juízo. Eu, porém, vos digo que qualquer que se irar contra seu irmão estará sujeito a juízo. Também qualquer que disser a seu irmão: Racá, será levado ao tribunal. E qualquer que o chamar de idiota estará sujeito ao fogo do inferno. Assim sendo, se trouxeres a tua oferta ao altar e te lembrares de que teu irmão tem alguma coisa contra ti, deixa ali mesmo diante do altar a tua oferta, e primeiro vai reconciliar-te com teu irmão, e depois volta e apresenta a tua oferta. Entra em acordo depressa com teu adversário, enquanto estás com ele a caminho do tribunal, para que não aconteça que o adversário te entregue ao juiz, o juiz te entregue ao carcereiro, e te joguem na cadeia. Com toda a certeza afirmo que de maneira alguma sairás dali, enquanto não pagares o último centavo. Adultério no coração
Ouvistes o que foi dito: Não cometerás adultério. Eu, porém, vos digo, que qualquer que olhar para uma mulher com intenção impura, em seu coração, já cometeu adultério com ela. Se o teu olho direito te leva a pecar, arranca-o e lança-o fora de ti; pois te é mais proveitoso perder um dos teus membros do que todo o teu corpo ser lançado no inferno. E, se tua mão direita te fizer pecar, corta-a e atira-a para longe de ti; pois te é melhor que um dos teus membros se perca do que todo o teu corpo seja lançado no inferno. O casamento é sagrado
Foi dito também: Aquele que se divorciar de sua esposa deverá dar a ela uma certidão de divórcio. Eu, porém, vos digo: Qualquer que se divorciar da sua esposa, exceto por imoralidade sexual, faz com que ela se torne adúltera, e quem se casar com a mulher divorciada estará cometendo adultério. Votos e juramentos
Também ouvistes o que foi dito aos antigos: Não jurarás falso, mas cumprirás rigorosamente teus juramentos ao Senhor. Entretanto, Eu vos afirmo: Não jureis de forma alguma; nem pelos céus, que são o trono de Deus; nem pela terra, por ser o estrado onde repousam seus pés; nem por Jerusalém, porque é a cidade do grande Rei. E não jures por tua cabeça, pois não tens o poder de tornar um fio de cabelo branco ou preto. Seja, porém, o teu sim, sim! E o teu não, não! O que passar disso vem do Maligno. Jamais use a vingança
Ouvistes o que foi dito: Olho por olho e dente por dente. Eu, porém, vos digo: Não resistais ao perverso; mas se alguém te ofender com um tapa na face direita, volta-lhe também a outra. E se alguém quiser processar-te e tirar-te a túnica, deixa que leve também a capa. Assim, se alguém te forçar a andar uma milha, vai com ele duas. Dá a quem te pedir e não te desvies de quem deseja que lhe emprestes algo. Ame os que o odeiam
Ouvistes o que foi dito: Amarás o teu próximo e odiarás o teu inimigo. Eu, porém, vos digo: Amai os vossos inimigos e orai pelos que vos perseguem; para que vos torneis filhos do vosso Pai que está nos céus, pois que Ele faz raiar o seu sol sobre maus e bons e derrama chuva sobre justos e injustos. Porque se amardes os que vos amam, que recompensa tendes? Não fazem os publicanos igualmente assim? E, se saudardes somente os vossos irmãos, que fazeis de notável? Não agem os gentios também dessa maneira? Assim sendo, sede vós perfeitos como perfeito é o vosso Pai que está nos céus.
Guardai-vos de fazer a vossa caridade e obras de justiça diante dos homens, com o fim de serem vistos por eles; caso contrário, não tereis qualquer recompensa do vosso Pai que está nos céus.
Por essa razão, quando deres um donativo, não toques trombeta diante de ti, como fazem os hipócritas, nas sinagogas e nas ruas, para serem glorificados pelos homens. Com toda a certeza vos afirmo que eles já receberam o seu galardão. Tu, porém, quando deres uma esmola ou ajuda, não deixes tua mão esquerda saber o que faz a direita. Para que a tua obra de caridade fique em secreto: e teu Pai, que vê em secreto, te recompensará. A oração modelo
E, quando orardes, não sejais como os hipócritas, pois que apreciam orar em pé nas sinagogas e nas esquinas das ruas, para serem admirados pelos outros. Com toda a certeza vos afirmo que eles já receberam o seu galardão. Tu, porém, quando orares, vai para teu quarto e, após ter fechado a porta, orarás a teu Pai, que está em secreto; e teu Pai, que vê em secreto, te recompensará plenamente.
E, quando orardes, não useis de vãs repetições, como fazem os pagãos; pois imaginam que devido ao seu muito falar serão ouvidos. Portanto, não vos assemelheis a eles; porque Deus, o vosso Pai, sabe tudo de que tendes necessidade, antes mesmo que lho peçais.
Por essa razão, vós orareis: Pai nosso, que estás nos céus! Santificado seja o teu Nome.
Venha o teu Reino. Seja feita a tua vontade, assim na terra como no céu.
Dá-nos hoje o nosso pão diário.
Perdoa-nos as nossas dívidas, assim como perdoamos aos nossos devedores.
E não nos conduzas à tentação, mas livra-nos do Maligno. Porque teu é o Reino, o poder e a glória para sempre. Amém. Pois, se perdoardes aos homens as suas ofensas, assim também vosso Pai celeste vos perdoará. Entretanto, se não perdoardes aos homens, tampouco vosso Pai vos perdoará as vossas ofensas. Jejuar é adorar a Deus
Quando jejuardes, não vos mostreis com aspecto sombrio como os hipócritas; pois desfiguram o rosto com a intenção de mostrar às pessoas que estão jejuando. Tu, porém, quando jejuares, unge tua cabeça e lava o rosto. Pois, assim, não parecerá aos outros que jejuas; e, sim, ao teu Pai em secreto; e teu Pai, que vê em secreto, te recompensará. Investir os recursos no céu
Não acumuleis para vós outros tesouros na terra, onde a traça e a ferrugem destroem, e onde ladrões arrombam para roubar. Mas ajuntai para vós outros tesouros no céu, onde a traça nem a ferrugem podem destruir, e onde os ladrões não arrombam e roubam. Porque, onde estiver o teu tesouro, aí também estará o teu coração. Um corpo iluminado
Os olhos são a lâmpada do corpo. Portanto, se teus olhos forem bons, teu corpo será pleno de luz. Porém, se teus olhos forem maus, todo o teu corpo estará em absoluta escuridão. Por isso, se a luz que está em ti são trevas, quão tremendas são essas trevas!SSE Servir somente a Deus
Ninguém pode servir a dois senhores; pois odiará um e amará o outro, ou será leal a um e desprezará o outro. Não podeis servir a Deus e a Mâmon. Descanso na providência divina
Portanto, vos afirmo: não andeis preocupados com a vossa própria vida, quanto ao que haveis de comer ou beber; nem pelo vosso corpo, quanto ao que haveis de vestir. Não é a vida mais do que o alimento, e o corpo mais do que as roupas? Contemplai as aves do céu: não semeiam, não colhem, nem armazenam em celeiros; contudo, vosso Pai celestial as sustenta. Não tendes vós muito mais valor do que as aves? Qual de vós, por mais que se preocupe, pode acrescentar algum tempo à jornada da sua vida? E por que andais preocupados quanto ao que vestir? Observai como crescem os lírios do campo. Eles não trabalham nem tecem. Eu, contudo, vos asseguro que nem Salomão, em todo o esplendor de sua glória, vestiu-se como um deles. Então, se Deus veste assim a erva do campo, que hoje existe e amanhã é lançada ao fogo, quanto mais a vós outros, homens de pequena fé? Portanto, não vos preocupeis, dizendo: Que iremos comer? Que iremos beber? Ou ainda: Com que nos vestiremos? Pois são os pagãos que tratam de obter tudo isso; mas vosso Pai celestial sabe que necessitais de todas essas coisas. Buscai, assim, em primeiro lugar, o Reino de Deus e a sua justiça, e todas essas coisas vos serão acrescentadas.
Portanto, não vos preocupeis com o dia de amanhã, pois o amanhã trará suas próprias preocupações. É suficiente o mal que cada dia traz em si mesmo.
Não julgueis, para que não sejais julgados. Pois com o critério com que julgardes, sereis julgados; e com a medida que usardes para medir a outros, igualmente medirão a vós. Por que reparas tu o cisco no olho de teu irmão, mas não percebes a viga que está no teu próprio olho? E como podes dizer a teu irmão: Permite-me remover o cisco do teu olho, quando há uma viga no teu? Hipócrita! Tira primeiro a trave do teu olho, e então poderás ver com clareza para tirar o cisco do olho de teu irmão.
Não deis o que é sagrado aos cães, nem jogueis aos porcos as vossas pérolas, para que não as pisoteiem e, voltando-se, vos façam em pedaços. Perseverança na oração
Pedi, e vos será concedido; buscai, e encontrareis; batei, e a porta será aberta para vós. Pois todo o que pede recebe; o que busca encontra; e a quem bate, se lhe abrirá. Ou qual dentre vós é o homem que, se o filho lhe pedir pão, lhe dará uma pedra? Ou se lhe pedir peixe, lhe entregará uma cobra? Assim, se vós, sendo maus, sabeis dar bons presentes aos vossos filhos, quanto mais vosso Pai que está nos céus dará o que é bom aos que lhe pedirem!
Portanto, tudo quanto quereis que as pessoas vos façam, assim fazei-o vós também a elas, pois esta é a Lei e os Profetas. Os dois únicos caminhos
Entrai pela porta estreita, pois larga é a porta e amplo o caminho que levam à perdição, e muitos são os que entram por esse caminho. Porque estreita é a porta e difícil o caminho que conduzem à vida, apenas uns poucos encontram esse caminho! Pelo fruto se conhece a árvore
Acautelai-vos quanto aos falsos profetas. Eles se aproximam de vós disfarçados de ovelhas, mas no seu íntimo são como lobos devoradores. Pelos seus frutos os conhecereis. É possível alguém colher uvas de um espinheiro ou figos das ervas daninhas? Assim sendo, toda árvore boa produz bons frutos, mas a árvore ruim dá frutos ruins. A árvore boa não pode dar frutos ruins, nem a árvore ruim produzir bons frutos. Toda árvore que não produz bons frutos é cortada e atirada ao fogo. Portanto, pelos seus frutos os conhecereis.
Nem todo aquele que diz a mim: Senhor, Senhor! entrará no Reino dos céus, mas somente o que faz a vontade de meu Pai, que está nos céus. Muitos dirão a mim naquele dia: Senhor, Senhor! Não temos nós profetizado em teu nome? Em teu nome não expulsamos demônios? E, em teu nome, não realizamos muitos milagres? Então lhes declararei: Nunca os conheci. Afastai-vos da minha presença, vós que praticais o mal. O sábio e o insensato
Assim, todo aquele que ouve estas minhas palavras e as pratica será comparado a um homem sábio, que construiu a sua casa sobre a rocha. E caiu a chuva, vieram as enchentes, sopraram os ventos e bateram com violência contra aquela casa, mas ela não caiu, pois tinha seus alicerces na rocha. Pois, todo aquele que ouve estas minhas palavras e não as pratica é como um insensato que construiu a sua casa sobre a areia. E caiu a chuva, vieram as enchentes, sopraram os ventos e bateram com violência contra aquela casa, e ela desabou. E grande foi a sua ruína.
Quando Jesus acabou de pronunciar estas palavras, estavam as multidões atônitas com o seu ensino. Porque Ele as ensinava como quem tem autoridade, e não como os mestres da lei.
"""

model_name = 'pierreguillou/bert-base-cased-squad-v1.1-portuguese'
nlp = pipeline("question-answering", model=model_name)

question = "Como conheço o lobo?"

result = nlp(question=question, context=context)

print(f"Answer: '{result['answer']}', score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']}")

# Answer: '1 de dezembro de 2019', score: 0.713, start: 328, end: 349